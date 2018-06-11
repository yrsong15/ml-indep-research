
# Machine Learning - Independent Research Study

### Intro

This is a repo containing files from my independent research study conducted during the Spring 2018 semester at Duke University. 

For theoretical research study on AI, Python files that run on simulated Minecraft settings were used to develop **search/learning algorithms** (minimax search & alpha-beta pruning, Markov models, Bayesian estimation, reinforcement learning, *etc.*) 

For Machine Learning applications, [Tensorflow](https://www.tensorflow.org/) and its pertinent libraries (*i.e.* NumPy, Pandas, and SciKit-Learn) were used primarily. Files are saved in a [Jupyter Notebook](http://jupyter.org/) format that can be run locally. 

### Search Algorithms

+ [BFS, DFS, Greedy Search](https://github.com/yrsong15/ml-indep-research/blob/master/search_algo/bfs_and_greedy_search.py)
+ [Constraint Satisfaction Problems (CSPs)](https://github.com/yrsong15/ml-indep-research/blob/master/search_algo/constraint_satisfaction_problem.py)
+ [Minimax search with Alpha-beta pruning](https://github.com/yrsong15/ml-indep-research/blob/master/search_algo/minimax_alphabeta.py)

### Learning Algorithms
+ [Confusion matrix generation](https://github.com/yrsong15/ml-indep-research/blob/master/learning_algo/train_test_prediction.py)
+ [Bayesian estimation algorithms](https://github.com/yrsong15/ml-indep-research/blob/master/learning_algo/learn_naive_bayes.py) that were used to predict [2017 NCAA Men's Basketball tournament outcomes](https://github.com/yrsong15/ml-indep-research/blob/master/learning_algo/bayes_ncaa_prediction.py) 
+ Reinforcement learning algorithms including [Q-learning](https://github.com/yrsong15/ml-indep-research/blob/master/learning_algo/q_learning_agents.py) and [value iteration](https://github.com/yrsong15/ml-indep-research/blob/master/learning_algo/value_iteration_agents.py), which were used to teach an agent to reach the goal state in a Minecraft environment that was previously completely unknown to the agent. 

### Tensorflow Projects

+ [Classifier](https://github.com/yrsong15/ml-indep-research/blob/master/tf_proj/MNIST.ipynb) that predicts handwritten numerical digits from the canonical MNIST dataset 
+ [Estimator](https://github.com/yrsong15/ml-indep-research/blob/master/tf_proj/Housing.ipynb) that predicts housing prices in the California real estate market
+ [Estimator](https://github.com/yrsong15/ml-indep-research/blob/master/tf_proj/Wine.ipynb) that predicts wine quality based on inputs including acidity and residual sugar
	+ Wine dataset obtained from the [UC Irvine Machine Learning Repo](https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/)

### Resources
+ **P. Norvig, S. Russell** - Artificial Intelligence: A Modern Approach
+ **A. Geron** - Hands-On Machine Learning with Scikit-Learn and Tensorflow
+ [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course/)
+ [Microsoft AI Online Courses](https://academy.microsoft.com/en-us/professional-program/tracks/artificial-intelligence/)
+ [UC Berkeley Data Science MOOC](https://www.edx.org/professional-certificate/berkeleyx-foundations-of-data-science#courses)
+ And of course, my lecture notes from Duke University coursework



