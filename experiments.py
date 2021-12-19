import doudizhu
import matplotlib.pyplot as pt

doudizhu.experiment_control = True

node_nums = []
score_list = []
for i in range(100):
    doudizhu.process_sum = 0
    score = doudizhu.play()
    node_nums.append(doudizhu.process_sum)
    score_list.append(score)

print(node_nums)
print(score_list)

pt.plot(node_nums, 'b-')
pt.legend(["processed nodes"])
pt.show()

res1 = []
res2 = []
res3 = []

for [a, b, c] in score_list:
      res1.append(a)
      res2.append(b)
      res3.append(c)

pt.figure()
pt.plot(res1, 'r-')
pt.plot(res2, 'g-')
pt.plot(res3, 'b-')
pt.legend(["tree-based", "baseline1", "baseline2"])
pt.show()
