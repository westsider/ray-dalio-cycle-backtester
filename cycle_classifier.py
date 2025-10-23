"""
Economic Cycle Classifier based on Ray Dalio's framework

Classifies the economy into four stages:
- Expansion: Growth accelerating, inflation moderate
- Peak: Growth slowing, inflation rising, tight credit
- Contraction: Negative growth, rising unemployment
- Recovery: Growth turning positive, unemployment falling
"""

import pandas as pd
import numpy as np
from enum import Enum


class CycleStage(Enum):
    """Economic cycle stages"""
    EXPANSION = "Expansion"
    PEAK = "Peak"
    CONTRACTION = "Contraction"
    RECOVERY = "Recovery"


class EconomicCycleClassifier:
    """
    Rule-based classifier for economic cycle stages

    Based on multiple indicators:
    - GDP growth rate
    - Unemployment rate and trend
    - Inflation rate
    - Yield curve (10Y - 2Y spread)
    - Interest rate trends
    """

    def __init__(self):
        self.classifications = None

    def classify(self, data):
        """
        Classify economic cycle stage for each time period

        Args:
            data: DataFrame with economic indicators

        Returns:
            Series with cycle stage classifications
        """
        print("Classifying economic cycle stages...")

        # Create a copy to avoid modifying original
        df = data.copy()

        # Calculate moving averages and trends for smoothing
        if 'GDP_GROWTH' in df.columns:
            df['GDP_GROWTH_MA'] = df['GDP_GROWTH'].rolling(window=90, min_periods=30).mean()
            df['GDP_TREND'] = df['GDP_GROWTH_MA'].diff(periods=90)

        if 'UNEMPLOYMENT' in df.columns:
            df['UNEMPLOYMENT_MA'] = df['UNEMPLOYMENT'].rolling(window=90, min_periods=30).mean()
            df['UNEMPLOYMENT_TREND'] = df['UNEMPLOYMENT_MA'].diff(periods=90)

        if 'INFLATION_RATE' in df.columns:
            df['INFLATION_MA'] = df['INFLATION_RATE'].rolling(window=90, min_periods=30).mean()

        if 'YIELD_CURVE' in df.columns:
            df['YIELD_CURVE_MA'] = df['YIELD_CURVE'].rolling(window=30, min_periods=10).mean()

        # Initialize with neutral state
        stages = pd.Series(index=df.index, dtype=object)

        # Classification logic for each row
        for idx in df.index:
            stage = self._classify_single_period(df.loc[idx])
            stages.loc[idx] = stage.value if stage else None

        # Forward fill missing values
        stages = stages.fillna(method='ffill')

        self.classifications = stages
        print(f"✓ Classified {len(stages)} periods")

        # Print summary
        if not stages.empty:
            print("\nCycle Distribution:")
            for stage in CycleStage:
                count = (stages == stage.value).sum()
                pct = (count / len(stages)) * 100
                print(f"  {stage.value}: {count} days ({pct:.1f}%)")

        return stages

    def _classify_single_period(self, row):
        """
        Classify a single time period based on indicator values

        Rules (simplified):
        1. CONTRACTION: Negative GDP growth OR rapidly rising unemployment
        2. RECOVERY: GDP turning positive, unemployment still high but falling
        3. EXPANSION: Positive GDP growth, falling/low unemployment, moderate inflation
        4. PEAK: Growth slowing, inflation rising, inverted yield curve
        """
        # Extract indicators with defaults if missing
        gdp_growth = row.get('GDP_GROWTH_MA', np.nan)
        gdp_trend = row.get('GDP_TREND', np.nan)
        unemployment = row.get('UNEMPLOYMENT_MA', np.nan)
        unemployment_trend = row.get('UNEMPLOYMENT_TREND', np.nan)
        inflation = row.get('INFLATION_MA', np.nan)
        yield_curve = row.get('YIELD_CURVE_MA', np.nan)

        # Skip if too many missing values
        missing_count = sum([np.isnan(x) for x in [gdp_growth, unemployment, inflation]])
        if missing_count > 1:
            return None

        # CONTRACTION: Negative growth or rapidly rising unemployment
        if (not np.isnan(gdp_growth) and gdp_growth < 0) or \
           (not np.isnan(unemployment_trend) and unemployment_trend > 0.3):
            return CycleStage.CONTRACTION

        # PEAK: Slowing growth, high inflation, inverted yield curve
        if (not np.isnan(gdp_trend) and gdp_trend < -0.5) and \
           (not np.isnan(inflation) and inflation > 3.5) or \
           (not np.isnan(yield_curve) and yield_curve < -0.2):
            return CycleStage.PEAK

        # RECOVERY: Positive but low growth, high unemployment but falling
        if (not np.isnan(gdp_growth) and 0 <= gdp_growth < 2) and \
           (not np.isnan(unemployment) and unemployment > 6) and \
           (not np.isnan(unemployment_trend) and unemployment_trend < -0.1):
            return CycleStage.RECOVERY

        # EXPANSION: Healthy growth, low/falling unemployment
        if (not np.isnan(gdp_growth) and gdp_growth >= 0) and \
           (not np.isnan(unemployment_trend) and unemployment_trend <= 0):
            return CycleStage.EXPANSION

        # Default to expansion if indicators are generally positive
        if (not np.isnan(gdp_growth) and gdp_growth > 0):
            return CycleStage.EXPANSION

        return None

    def get_cycle_changes(self):
        """
        Get dates when the cycle stage changed

        Returns:
            DataFrame with cycle transitions
        """
        if self.classifications is None:
            return None

        changes = self.classifications != self.classifications.shift(1)
        transitions = self.classifications[changes].to_frame('stage')
        transitions['prev_stage'] = self.classifications.shift(1)[changes]

        return transitions

    def get_current_stage(self):
        """Get the most recent cycle stage"""
        if self.classifications is None or self.classifications.empty:
            return None
        return self.classifications.iloc[-1]
