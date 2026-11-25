"""Matched response comparisons on 1995 published marker interpolants."""
import numpy as np
from scipy.special import ndtr
from v742_v751.model import spectrum, MARKS

CASES = [
 ('全覆盖铝片','0.4 mm 铝，正入射，T=exp(−μd)'),
 ('全覆盖铜片','0.25 mm 铜，正入射，T=exp(−μd)'),
 ('串联铝铜','0.7 mm 铝与 0.25 mm 铜全覆盖，光学厚度相加'),
 ('带孔铜片','一半射线走开孔，其余穿过 0.25 mm 铜，通量透射按路径比例求和'),
 ('斜射角积分','0.7 mm 铝与 0.25 mm 铜，角度至 atan(7.98/9.91)，以 cos³θ sinθ 为权平均透射'),
 ('锗表面非活性层','取 40 μm 锗的出射总路径，使用总衰减系数'),
 ('有限敏感厚度','0.4 mm 有效锗层，采用至少一次相互作用概率 1−exp(−μd)；它只代理全能峰效率'),
 ('近阈值选择','以 34.5 keV 为示例离线下阈，σ=0.5 keV，取高斯累积分布作接受率'),
 ('有限分辨率能窗','对真能量位于带内的事件，以 σ=0.5 keV 计算读数留在 34.5–36.5 keV 的概率，不计窗外迁入'),
 ('复合符合选择','角平均铝铜透射、锗相互作用效率和有限分辨率留窗概率相乘，假设条件独立')]
QUESTIONS=[
 ('谱内极差','在固定能窗求最大与最小接受率之比；它约束该候选权重可以多陡。'),
 ('绝对接受率','对平坦真谱积分 T 并除以带宽；共同绝对损失与相对谱形可有不同量级。'),
 ('观测交叉比','四条已发表谱分别乘 T 后积分，比较方向比之比与原始值。属于敏感性扰动。'),
 ('反向效率修正','对各条谱乘 1/T，检验把已选谱视作待展开谱时的方向和幅度；极低效率会放大误差。'),
 ('两线方向迁移','分别计算两条入射线 D2/D1 的变化倍数；两者之比才是总交叉比变化。'),
 ('连续开启响应','令权重为 T 的 λ 次方；在 λ=0 的对数交叉比导数等于各谱 ln T 均值的带符号和。'),
 ('不依赖谱形的界','设 K=max T/min T。各谱平均权重都落在相同区间，故交叉比对数变化绝对值不超过 2 ln K。'),
 ('独立参考的计数预算','两端等曝光平坦输入并忽略入射通量误差；每端 N 个入射泊松期望，端点对数透射比方差约为 (1/T低+1/T高)/N。求标准差 0.05 所需 N。'),
 ('避开边缘的留出窗','将积分区间收窄到 35–36 keV，沿用原来的 T 函数及原阈值，复核中心区域的响应偏移。'),
 ('响应与恒等模型的可区分性','若仅测两端且允许未知共同通量，拟合常数效率。再冻结它，计算带中心对该常数的相对偏差；中心可作为独立参考点。')]
LIMITS=['真实射线有一部分穿孔。','等厚全覆盖未包含双锥孔。','原装置各层厚度不能视为所有事件都经过的厚度。','开孔比例是假定值，需分方向测量。','同层平板模型未重建锥孔、胶和金插片。','总路径取设计值，未取得逐台死层厚度。','散射逃逸会使全能峰效率低于相互作用概率。','该阈值是人为压力测试，与论文约 8 keV 硬件阈值不同。','真实响应含窗外迁入及非高斯尾。','各因素在真实探测器内可能相关，乘积模型须另行校准。']

def response(case,e):
    def mu(a,b,rho):
        return rho*a*(e/30)**(np.log(b/a)/np.log(40/30))
    al=mu(1.128,.5685,2.70)
    cu=mu(10.92,4.862,8.96)
    ge=mu(13.85,6.207,5.323)
    tau=.07*al+.025*cu
    if case==0: return np.exp(-.04*al)
    if case==1: return np.exp(-.025*cu)
    if case==2: return np.exp(-tau)
    if case==3: return .5*(1+np.exp(-.025*cu))
    if case==5: return np.exp(-.004*ge)
    interaction=-np.expm1(-.04*ge)
    if case==6: return interaction
    if case==7: return ndtr((e-34.5)/.5)
    window=ndtr((36.5-e)/.5)-ndtr((34.5-e)/.5)
    if case==8: return window
    nodes,w=np.polynomial.legendre.leggauss(32)
    low=1/np.hypot(1,7.98/9.91)
    u=low+(nodes+1)*(1-low)/2
    angular=np.average(np.exp(-tau[:,None]/u),axis=1,weights=w*u**3)
    return angular if case==4 else angular*interaction*window

def compute(case,n=2001):
    def band(lo,hi):
        e=np.linspace(lo,hi,n)
        y=np.array([spectrum(k,e) for k in MARKS])
        y[:,[0,-1]]*=.5
        t=response(case,e)
        return e,y,t
    e,y,t=band(34.5,36.5)
    sign=np.array([1,-1,-1,1])
    def contrast(y,w): return float(sign@np.log(y@w))
    ones=np.ones(n)
    base=contrast(y,ones)
    av=(y@t)/y.sum(1)
    span=float(t.max()/t.min())
    _,inner,tw=band(35,36)
    slope=float(sign@((y@np.log(t))/y.sum(1)))
    h=.0001
    return [
      {'span':span,'end_ratio':float(t[-1]/t[0])},
      {'flat_acceptance':float(np.trapezoid(t,e)/(e[-1]-e[0]))},
      {'original':float(np.exp(base)),'weighted':float(np.exp(contrast(y,t)))},
      {'inverse_weighted':float(np.exp(contrast(y,1/t)))},
      {'high_line':float(av[1]/av[0]),'low_line':float(av[3]/av[2])},
      {'derivative':slope,'finite_difference':(contrast(y,t**h)-contrast(y,t**-h))/(2*h)},
      {'bound':float(2*np.log(span)),'actual':abs(contrast(y,t)-base)},
      {'incident_per_endpoint':int(np.ceil((1/t[0]+1/t[-1])/.05**2))},
      {'narrow_log_shift':contrast(inner,tw)-contrast(inner,ones),'full_log_shift':contrast(y,t)-base},
      {'constant_fit':float((t[0]+t[-1])/2),'midpoint_relative_residual':float(2*t[n//2]/(t[0]+t[-1])-1)}]
