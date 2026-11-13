from models.joint_calibration import *
base=Design()
scenarios=[('基准',base,(1,1)),('主实验曝光×3',Design(t=3), (1,1)),('校准数据×3',Design(k_eta=300,k_beta=300),(1,1)),('效率校准低估5%',base,(0.95,1))]
for i,(name,d,bias) in enumerate(scenarios):
 r=bootstrap(d,n_null=199,n_alt=199,eps=1.,alpha=.05,seed=20261112+i,evaluation_bias=bias)
 print(name,r['threshold'],r['fpr'],wilson(round(r['fpr']*199),199),r['power'],wilson(round(r['power']*199),199))
