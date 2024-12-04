from scipy.optimize import minimize
import pandas as pd
import numpy as np
from scipy.optimize import linprog

# 假設 csv 內容
df = pd.read_csv('trimed_data.csv')  # 請換成實際的 CSV 路徑

# 投手策略（code）
pitcher_strategies = ['F', 'B', 'O']
batter_strategies = ['Swing', 'No Swing']
num_batter_strategies = len(batter_strategies)
num_pitcher_strategies = len(pitcher_strategies)
# 生成收益矩陣，打者行，投手列
payoff_matrix = np.zeros((len(batter_strategies), len(pitcher_strategies)))


# 填充收益矩陣
for i, swing in enumerate([1, 0]):  # 1: 揮棒, 0: 不揮棒
    for j, pitch in enumerate(pitcher_strategies):
        subset = df[(df['pitch_type'] == pitch) & (df['swing'] == swing)]
        payoff_matrix[i, j] = subset['bat_result'].mean(
        ) if not subset.empty else 0

print(payoff_matrix)


def find_nash_equilibrium(payoff_matrix, tolerance=1e-6, max_iterations=1000):
    num_batter_strategies, num_pitcher_strategies = payoff_matrix.shape

    # 初始化混合策略
    batter_strategy = np.full(num_batter_strategies,
                              1 / num_batter_strategies)  # 均勻分佈
    pitcher_strategy = np.full(
        num_pitcher_strategies, 1 / num_pitcher_strategies)  # 均勻分佈

    for iteration in range(max_iterations):
        # 計算打者的最佳混合策略
        c_batter = np.zeros(num_batter_strategies + 1)
        c_batter[-1] = -1  # 最大化 min_payoff

        A_ub_batter = np.hstack(
            [-payoff_matrix.T, np.ones((num_pitcher_strategies, 1))])
        b_ub_batter = np.zeros(num_pitcher_strategies)

        A_eq_batter = np.zeros((1, num_batter_strategies + 1))
        A_eq_batter[0, :num_batter_strategies] = 1
        b_eq_batter = np.array([1])

        bounds_batter = [(0, 1) for _ in range(
            num_batter_strategies)] + [(None, None)]

        res_batter = linprog(c_batter, A_ub=A_ub_batter, b_ub=b_ub_batter,
                             A_eq=A_eq_batter, b_eq=b_eq_batter, bounds=bounds_batter, method='highs')
        new_batter_strategy = res_batter.x[:-1]

        # 計算投手的最佳混合策略
        payoff_matrix_pitcher = 1 - payoff_matrix  # 投手收益矩陣
        c_pitcher = np.zeros(num_pitcher_strategies + 1)
        c_pitcher[-1] = -1  # 最大化 min_payoff

        A_ub_pitcher = np.hstack(
            [-payoff_matrix_pitcher, np.ones((num_batter_strategies, 1))])
        b_ub_pitcher = np.zeros(num_batter_strategies)

        A_eq_pitcher = np.zeros((1, num_pitcher_strategies + 1))
        A_eq_pitcher[0, :num_pitcher_strategies] = 1
        b_eq_pitcher = np.array([1])

        bounds_pitcher = [(0, 1) for _ in range(
            num_pitcher_strategies)] + [(None, None)]

        res_pitcher = linprog(c_pitcher, A_ub=A_ub_pitcher, b_ub=b_ub_pitcher,
                              A_eq=A_eq_pitcher, b_eq=b_eq_pitcher, bounds=bounds_pitcher, method='highs')
        new_pitcher_strategy = res_pitcher.x[:-1]

        # 檢查是否收斂
        if (np.linalg.norm(new_batter_strategy - batter_strategy) < tolerance and
                np.linalg.norm(new_pitcher_strategy - pitcher_strategy) < tolerance):
            print(f"Converged in {iteration + 1} iterations.")
            return new_batter_strategy, new_pitcher_strategy

        print(new_batter_strategy)
        print(new_pitcher_strategy)
        # 更新策略
        batter_strategy = new_batter_strategy
        pitcher_strategy = new_pitcher_strategy

    raise ValueError(
        "Did not converge to a Nash equilibrium within the maximum number of iterations.")


batter_strategy, pitcher_strategy = find_nash_equilibrium(payoff_matrix)

print("打者的混合策略:", batter_strategy)
print("投手的混合策略:", pitcher_strategy)
