import math

class MatchPredictor:
    def get_poisson_probability(self, actual, expected):
        """Calculates the probability of a specific goal count."""
        if expected <= 0: expected = 0.01
        return (math.exp(-expected) * (expected**actual)) / math.factorial(actual)

    def calculate_probability(self, home_stats, away_stats):
        """
        Dynamically calculates win probabilities using live league stats.
        Uses API keys: goalsFor, goalsAgainst, playedGames.
        """
        # Calibrated constants for 2026 parity
        league_avg_goals = 1.38 
        home_field_advantage = 1.22 
        draw_bias = 0.12            

        # Attack/Defense Strength Ratios
        h_atk = (home_stats['goalsFor'] / home_stats['playedGames']) / league_avg_goals
        h_def = (home_stats['goalsAgainst'] / home_stats['playedGames']) / league_avg_goals
        a_atk = (away_stats['goalsFor'] / away_stats['playedGames']) / league_avg_goals
        a_def = (away_stats['goalsAgainst'] / away_stats['playedGames']) / league_avg_goals

        # Expected Goals (xG) Calculation
        h_xg = h_atk * a_def * league_avg_goals * home_field_advantage
        a_xg = a_atk * h_def * league_avg_goals

        # 8x8 Poisson Matrix Simulation
        h_win, a_win, draw = 0, 0, 0
        for i in range(8):
            for j in range(8):
                prob = self.get_poisson_probability(i, h_xg) * \
                       self.get_poisson_probability(j, a_xg)
                if i > j: h_win += prob
                elif j > i: a_win += prob
                else: draw += (prob * (1 + draw_bias))

        total = h_win + a_win + draw
        return {
            "Home": round((h_win / total) * 100, 1),
            "Away": round((a_win / total) * 100, 1),
            "Draw": round((draw / total) * 100, 1),
            "h_xg": round(h_xg, 2),
            "a_xg": round(a_xg, 2)
        }