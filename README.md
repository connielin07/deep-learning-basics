## Merge logic-gates-perceptron, mlp-prediction repos to new repo deep-learning-basics:
touch README.md
git add README.md
git commit -m "initial commit"

# logic repo
git remote add old_logic https://github.com/connielin07/logic-gates-perceptron.git
git fetch old_logic
git subtree add --prefix=ch1-logic-gates-perceptron old_logic main

# mlp repo
git remote add old-mlp https://github.com/connielin07/mlp-prediction.git
git fetch old-mlp
git subtree add --prefix=ch2-mlp-prediction old_mlp main