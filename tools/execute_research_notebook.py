"""Execute a research notebook in a fresh process with a socket-free ipykernel."""
import io
import sys
from pathlib import Path

from ipykernel.inprocess.manager import InProcessKernelManager
import nbformat

path = Path(sys.argv[1])
book = nbformat.read(path, as_version=4)
km = InProcessKernelManager()
km.start_kernel()
client = km.client()
client.start_channels()
try:
    for cell in book.cells:
        if cell.cell_type != "code":
            continue
        cell.outputs, cell.execution_count = [], None
        stdout, stderr = io.StringIO(), io.StringIO()
        km.kernel.stdout, km.kernel.stderr = stdout, stderr
        msg_id = client.execute(cell.source)
        while True:
            msg = client.get_iopub_msg(timeout=30)
            if msg['parent_header'].get('msg_id') != msg_id:
                continue
            kind, data = msg["msg_type"], msg["content"]
            if kind == "status" and data["execution_state"] == "idle":
                break
            if kind == "execute_input":
                cell.execution_count = data["execution_count"]
            if kind in ("stream", "error", "display_data", "execute_result"):
                cell.outputs.append(nbformat.v4.output_from_msg(msg))
        for name, stream in (("stdout", stdout), ("stderr", stderr)):
            if stream.getvalue():
                cell.outputs.append(nbformat.v4.new_output(
                    "stream", name=name, text=stream.getvalue()))
        reply = client.get_shell_msg(timeout=30)["content"]
        if reply["status"] != "ok":
            raise RuntimeError(reply)
        if cell.execution_count is None:
            cell.execution_count = reply["execution_count"]
finally:
    client.stop_channels()
    km.shutdown_kernel()
nbformat.validate(book)
nbformat.write(book, path)
print([c.execution_count for c in book.cells if c.cell_type == "code"])
