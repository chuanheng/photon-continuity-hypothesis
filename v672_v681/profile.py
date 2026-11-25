"""Local identifiability for a fractional intensity coupling at eight selected points."""
import numpy as np

def profile(figures):
    points = [p for fig in figures.values() for p in fig["points"]]
    values = np.array([p["cross_section"] for p in points])
    # Standardize only for conditioning. This is a design calculation, not a fit.
    widths = np.array([(p["upper_plotted_error_endpoint"] - p["lower_plotted_error_endpoint"]) / 2 for p in points])
    column = values / widths
    design = np.column_stack((column, column))
    return {"points": len(points), "response_rank": int(np.linalg.matrix_rank(design)),
            "profiled_scale_residual": float(np.linalg.norm(design @ [1., -1.])),
            "known_scale_column_norm": float(np.linalg.norm(column))}
