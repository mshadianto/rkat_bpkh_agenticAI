"""
Prediction Models for Bank Muamalat
Machine learning models for forecasting and predictive analytics
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')
import logging

logger = logging.getLogger(__name__)

class NPFPredictionModel:
    """
    Model to predict NPF (Non-Performing Financing) trends
    """
    
    def __init__(self):
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.feature_columns = []
        self.is_trained = False
        
    def prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare features for NPF prediction
        """
        features = pd.DataFrame()
        
        # Lag features
        for lag in [1, 3, 6, 12]:
            features[f'npf_lag_{lag}'] = data['npf'].shift(lag)
            
        # Economic indicators
        features['gdp_growth'] = data.get('gdp_growth', 5.0)
        features['inflation'] = data.get('inflation', 3.0)
        features['bi_rate'] = data.get('bi_rate', 5.5)
        features['unemployment'] = data.get('unemployment', 5.0)
        
        # Bank-specific features
        features['car'] = data.get('car', 20.0)
        features['fdr'] = data.get('fdr', 85.0)
        features['bopo'] = data.get('bopo', 85.0)
        features['market_share'] = data.get('market_share', 1.5)
        
        # Time features
        features['month'] = pd.to_datetime(data.index).month
        features['quarter'] = pd.to_datetime(data.index).quarter
        features['year'] = pd.to_datetime(data.index).year
        
        # Rolling statistics
        features['npf_ma_3'] = data['npf'].rolling(window=3).mean()
        features['npf_ma_6'] = data['npf'].rolling(window=6).mean()
        features['npf_std_6'] = data['npf'].rolling(window=6).std()
        
        # Trend features
        features['npf_trend'] = self._calculate_trend(data['npf'], window=6)
        
        # Drop NaN values
        features = features.dropna()
        
        self.feature_columns = features.columns.tolist()
        
        return features
        
    def train(self, historical_data: pd.DataFrame):
        """
        Train the NPF prediction model
        """
        logger.info("Training NPF prediction model...")
        
        # Prepare features
        X = self.prepare_features(historical_data)
        y = historical_data['npf'].loc[X.index]
        
        # Time series split
        tscv = TimeSeriesSplit(n_splits=5)
        scores = []
        
        for train_idx, val_idx in tscv.split(X):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_val_scaled = self.scaler.transform(X_val)
            
            # Train model
            self.model.fit(X_train_scaled, y_train)
            
            # Validate
            y_pred = self.model.predict(X_val_scaled)
            mae = mean_absolute_error(y_val, y_pred)
            scores.append(mae)
            
        # Final training on all data
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        
        self.is_trained = True
        
        logger.info(f"Model trained. Average MAE: {np.mean(scores):.4f}")
        
        # Feature importance
        self.feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
    def predict(
        self,
        current_data: pd.DataFrame,
        horizon: int = 12
    ) -> Dict[str, Any]:
        """
        Predict NPF for future periods
        """
        if not self.is_trained:
            # Use simple time series model if not trained
            return self._simple_forecast(current_data, horizon)
            
        predictions = []
        prediction_intervals = []
        
        # Start with current data
        working_data = current_data.copy()
        
        for i in range(horizon):
            # Prepare features for prediction
            X = self.prepare_features(working_data)
            
            if len(X) == 0:
                # Fallback to simple forecast
                return self._simple_forecast(current_data, horizon)
                
            # Get latest features
            X_latest = X.iloc[[-1]]
            X_scaled = self.scaler.transform(X_latest)
            
            # Predict
            npf_pred = self.model.predict(X_scaled)[0]
            
            # Calculate prediction interval (simplified)
            std_error = 0.5  # Simplified standard error
            lower_bound = max(0, npf_pred - 1.96 * std_error)
            upper_bound = npf_pred + 1.96 * std_error
            
            predictions.append(npf_pred)
            prediction_intervals.append((lower_bound, upper_bound))
            
            # Add prediction to working data for next iteration
            next_date = working_data.index[-1] + pd.DateOffset(months=1)
            working_data.loc[next_date, 'npf'] = npf_pred
            
        # Generate forecast dates
        last_date = current_data.index[-1]
        forecast_dates = pd.date_range(
            start=last_date + pd.DateOffset(months=1),
            periods=horizon,
            freq='M'
        )
        
        return {
            'forecast': pd.Series(predictions, index=forecast_dates),
            'prediction_intervals': prediction_intervals,
            'forecast_dates': forecast_dates,
            'model_type': 'GradientBoosting',
            'feature_importance': self.feature_importance.head(10).to_dict('records') if hasattr(self, 'feature_importance') else None
        }
        
    def _calculate_trend(self, series: pd.Series, window: int) -> pd.Series:
        """Calculate trend using linear regression"""
        trend = pd.Series(index=series.index, dtype=float)
        
        for i in range(window, len(series)):
            y = series.iloc[i-window:i].values
            x = np.arange(window)
            
            if len(y) == window and not np.isnan(y).any():
                slope, _ = np.polyfit(x, y, 1)
                trend.iloc[i] = slope
                
        return trend
        
    def _simple_forecast(
        self,
        current_data: pd.DataFrame,
        horizon: int
    ) -> Dict[str, Any]:
        """Simple time series forecast as fallback"""
        npf_series = current_data['npf'].dropna()
        
        # Calculate trend
        x = np.arange(len(npf_series))
        y = npf_series.values
        slope, intercept = np.polyfit(x, y, 1)
        
        # Generate forecasts
        forecast_x = np.arange(len(npf_series), len(npf_series) + horizon)
        forecasts = slope * forecast_x + intercept
        
        # Add some randomness based on historical volatility
        std = npf_series.std()
        forecasts = np.maximum(0, forecasts + np.random.normal(0, std * 0.5, horizon))
        
        # Generate dates
        last_date = current_data.index[-1]
        forecast_dates = pd.date_range(
            start=last_date + pd.DateOffset(months=1),
            periods=horizon,
            freq='M'
        )
        
        return {
            'forecast': pd.Series(forecasts, index=forecast_dates),
            'prediction_intervals': [(f - std, f + std) for f in forecasts],
            'forecast_dates': forecast_dates,
            'model_type': 'SimpleTrend'
        }

class ProfitabilityPredictionModel:
    """
    Model to predict profitability metrics (ROA, ROE)
    """
    
    def __init__(self):
        self.roa_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.roe_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        
    def prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for profitability prediction"""
        features = pd.DataFrame(index=data.index)
        
        # Financial ratios
        features['npf'] = data.get('npf', 3.0)
        features['car'] = data.get('car', 20.0)
        features['fdr'] = data.get('fdr', 85.0)
        features['bopo'] = data.get('bopo', 85.0)
        features['nim'] = data.get('nim', 5.0)
        
        # Asset quality indicators
        features['provision_coverage'] = data.get('provision_coverage', 100.0)
        features['cost_of_funds'] = data.get('cost_of_funds', 4.0)
        
        # Market conditions
        features['bi_rate'] = data.get('bi_rate', 5.5)
        features['gdp_growth'] = data.get('gdp_growth', 5.0)
        features['competition_index'] = data.get('competition_index', 50.0)
        
        # Lag features
        if 'roa' in data.columns:
            features['roa_lag_1'] = data['roa'].shift(1)
            features['roa_lag_3'] = data['roa'].shift(3)
            
        if 'roe' in data.columns:
            features['roe_lag_1'] = data['roe'].shift(1)
            features['roe_lag_3'] = data['roe'].shift(3)
            
        return features.dropna()
        
    def predict_profitability(
        self,
        current_metrics: Dict[str, float],
        horizon: int = 4  # quarters
    ) -> Dict[str, Any]:
        """Predict ROA and ROE for future quarters"""
        
        # Create feature dataframe
        features = pd.DataFrame([current_metrics])
        
        # Prepare base features
        base_features = {
            'npf': current_metrics.get('npf', 3.99),
            'car': current_metrics.get('car', 29.42),
            'fdr': current_metrics.get('fdr', 85.0),
            'bopo': current_metrics.get('bopo', 98.5),
            'nim': current_metrics.get('nim', 4.5),
            'provision_coverage': current_metrics.get('provision_coverage', 100.0),
            'cost_of_funds': current_metrics.get('cost_of_funds', 4.0),
            'bi_rate': current_metrics.get('bi_rate', 5.5),
            'gdp_growth': current_metrics.get('gdp_growth', 5.0),
            'competition_index': 50.0,
            'roa_lag_1': current_metrics.get('roa', 0.03),
            'roa_lag_3': current_metrics.get('roa', 0.03),
            'roe_lag_1': current_metrics.get('roe', 0.4),
            'roe_lag_3': current_metrics.get('roe', 0.4)
        }
        
        # Generate predictions
        roa_predictions = []
        roe_predictions = []
        
        for quarter in range(horizon):
            # Simulate feature evolution
            # NPF expected to improve
            base_features['npf'] *= 0.95
            # BOPO expected to improve with digitalization
            base_features['bopo'] *= 0.98
            
            # Simple linear models for demonstration
            roa_pred = self._predict_roa(base_features)
            roe_pred = self._predict_roe(base_features)
            
            roa_predictions.append(roa_pred)
            roe_predictions.append(roe_pred)
            
            # Update lag features
            base_features['roa_lag_1'] = roa_pred
            base_features['roe_lag_1'] = roe_pred
            
        return {
            'roa_forecast': roa_predictions,
            'roe_forecast': roe_predictions,
            'forecast_periods': [f'Q{i+1}' for i in range(horizon)],
            'key_assumptions': {
                'npf_improvement': '5% per quarter',
                'bopo_improvement': '2% per quarter',
                'economic_growth': 'Stable at 5%'
            }
        }
        
    def _predict_roa(self, features: Dict[str, float]) -> float:
        """Predict ROA using simplified model"""
        # Simplified formula based on key drivers
        base_roa = 1.5  # Target ROA
        
        # Negative impact from NPF
        npf_impact = -(features['npf'] - 2.0) * 0.2
        
        # Negative impact from BOPO
        bopo_impact = -(features['bopo'] - 80.0) * 0.02
        
        # Positive impact from NIM
        nim_impact = (features['nim'] - 4.0) * 0.1
        
        roa = base_roa + npf_impact + bopo_impact + nim_impact
        
        # Add some momentum from previous ROA
        roa = 0.7 * roa + 0.3 * features['roa_lag_1']
        
        return max(0, min(3.0, roa))  # Cap between 0 and 3%
        
    def _predict_roe(self, features: Dict[str, float]) -> float:
        """Predict ROE using simplified model"""
        # ROE = ROA * Equity Multiplier
        roa = self._predict_roa(features)
        
        # Estimate equity multiplier based on CAR
        equity_multiplier = 100 / features['car']  # Simplified
        
        roe = roa * equity_multiplier * 10  # Scaling factor
        
        # Add momentum
        roe = 0.7 * roe + 0.3 * features['roe_lag_1']
        
        return max(0, min(25.0, roe))  # Cap between 0 and 25%

class CARPredictionModel:
    """
    Model to predict Capital Adequacy Ratio trajectory
    """
    
    def __init__(self):
        self.model = Ridge(alpha=1.0)
        self.is_trained = False
        
    def predict_car_trajectory(
        self,
        current_car: float,
        current_npf: float,
        profit_forecast: List[float],
        asset_growth_rate: float = 0.09,  # 9% annual
        dividend_payout_ratio: float = 0.3,
        horizon: int = 12  # months
    ) -> Dict[str, Any]:
        """
        Predict CAR trajectory based on profit forecasts and asset growth
        """
        car_projections = []
        car_current = current_car
        
        # Monthly rates
        monthly_asset_growth = (1 + asset_growth_rate) ** (1/12) - 1
        
        for month in range(horizon):
            # Estimate monthly profit (from quarterly forecast)
            quarter = month // 3
            monthly_profit = profit_forecast[min(quarter, len(profit_forecast)-1)] / 3
            
            # Calculate retained earnings
            retained_earnings = monthly_profit * (1 - dividend_payout_ratio)
            
            # Impact on capital
            capital_increase = retained_earnings * 0.01  # Percentage points
            
            # Asset growth impact (dilutes CAR)
            car_dilution = car_current * monthly_asset_growth
            
            # NPF impact (provisioning reduces capital)
            npf_impact = 0.1 if current_npf > 3 else 0  # Simplified
            
            # New CAR
            car_new = car_current + capital_increase - car_dilution - npf_impact
            
            car_projections.append(car_new)
            car_current = car_new
            
        return {
            'car_forecast': car_projections,
            'minimum_car': min(car_projections),
            'end_car': car_projections[-1],
            'months_below_minimum': sum(1 for car in car_projections if car < 12.0),
            'capital_needed': max(0, (12.0 - min(car_projections)) * 1e12)  # in IDR
        }

class CustomerBehaviorModel:
    """
    Model to predict customer behavior and deposit flows
    """
    
    def __init__(self):
        self.deposit_model = RandomForestRegressor(n_estimators=50)
        self.churn_threshold = 0.3
        
    def predict_deposit_growth(
        self,
        historical_deposits: pd.Series,
        economic_indicators: Dict[str, float],
        competitive_rates: Dict[str, float],
        horizon: int = 6
    ) -> Dict[str, Any]:
        """
        Predict deposit growth based on various factors
        """
        # Calculate historical growth rate
        growth_rates = historical_deposits.pct_change().dropna()
        avg_growth = growth_rates.mean()
        volatility = growth_rates.std()
        
        # Adjust for economic factors
        gdp_impact = (economic_indicators.get('gdp_growth', 5.0) - 5.0) * 0.002
        rate_impact = (competitive_rates.get('competitor_avg', 6.0) - 
                      competitive_rates.get('muamalat_rate', 5.5)) * -0.01
        
        # Base growth rate
        base_growth = avg_growth + gdp_impact + rate_impact
        
        # Generate projections with uncertainty
        projections = []
        current_value = historical_deposits.iloc[-1]
        
        for month in range(horizon):
            # Add randomness based on historical volatility
            monthly_growth = base_growth + np.random.normal(0, volatility)
            
            # Seasonal adjustment (higher in Ramadan/Hajj season)
            month_number = (datetime.now().month + month) % 12
            if month_number in [3, 4, 11, 12]:  # Ramadan and Hajj months
                monthly_growth *= 1.2
                
            new_value = current_value * (1 + monthly_growth)
            projections.append(new_value)
            current_value = new_value
            
        return {
            'deposit_forecast': projections,
            'expected_growth_rate': base_growth * 12,  # Annualized
            'volatility': volatility,
            'seasonal_factors': 'Higher growth expected during Ramadan and Hajj seasons',
            'risk_factors': self._identify_deposit_risks(base_growth)
        }
        
    def predict_customer_churn(
        self,
        customer_features: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Predict customer churn probability
        """
        # Simplified churn scoring based on key factors
        churn_scores = []
        
        risk_factors = {
            'low_balance': customer_features['balance'] < 10_000_000,  # 10M IDR
            'inactive': customer_features['months_inactive'] > 3,
            'single_product': customer_features['product_count'] == 1,
            'no_salary': ~customer_features['salary_account'],
            'young_relationship': customer_features['tenure_months'] < 12
        }
        
        for idx, row in customer_features.iterrows():
            score = 0
            
            # Calculate risk score
            if row['balance'] < 10_000_000:
                score += 0.3
            if row['months_inactive'] > 3:
                score += 0.3
            if row['product_count'] == 1:
                score += 0.2
            if not row.get('salary_account', False):
                score += 0.1
            if row['tenure_months'] < 12:
                score += 0.1
                
            churn_scores.append(min(score, 1.0))
            
        # Aggregate statistics
        high_risk_customers = sum(1 for score in churn_scores if score > self.churn_threshold)
        
        return {
            'average_churn_probability': np.mean(churn_scores),
            'high_risk_customers': high_risk_customers,
            'high_risk_percentage': (high_risk_customers / len(customer_features)) * 100,
            'key_churn_drivers': [
                'Low account balance',
                'Account inactivity',
                'Single product holding',
                'No salary domiciliation',
                'Short tenure'
            ],
            'retention_recommendations': self._generate_retention_strategies()
        }
        
    def _identify_deposit_risks(self, growth_rate: float) -> List[str]:
        """Identify risks to deposit growth"""
        risks = []
        
        if growth_rate < 0:
            risks.append("Negative growth trend")
        if growth_rate < 0.01:  # Less than 1% monthly
            risks.append("Below industry average growth")
            
        risks.extend([
            "Competition from digital banks",
            "Rising interest rates at competitors",
            "Economic uncertainty"
        ])
        
        return risks
        
    def _generate_retention_strategies(self) -> List[Dict[str, str]]:
        """Generate customer retention strategies"""
        return [
            {
                'strategy': 'Salary Account Campaign',
                'description': 'Offer incentives for salary domiciliation',
                'expected_impact': 'Reduce churn by 30%'
            },
            {
                'strategy': 'Product Bundling',
                'description': 'Cross-sell Hajj savings and investment products',
                'expected_impact': 'Increase product holding to 2.5 average'
            },
            {
                'strategy': 'Digital Engagement',
                'description': 'Enhance mobile app with personalized features',
                'expected_impact': 'Increase active users by 40%'
            },
            {
                'strategy': 'Loyalty Program',
                'description': 'Launch points-based rewards for transactions',
                'expected_impact': 'Improve retention by 25%'
            }
        ]

class ScenarioAnalysisModel:
    """
    Model for comprehensive scenario analysis
    """
    
    def __init__(self):
        self.models = {
            'npf': NPFPredictionModel(),
            'profitability': ProfitabilityPredictionModel(),
            'car': CARPredictionModel(),
            'deposits': CustomerBehaviorModel()
        }
        
    def run_scenario_analysis(
        self,
        base_metrics: Dict[str, float],
        scenarios: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Run comprehensive scenario analysis
        """
        results = {}
        
        for scenario_name, scenario_params in scenarios.items():
            logger.info(f"Running scenario: {scenario_name}")
            
            # Adjust base metrics for scenario
            scenario_metrics = base_metrics.copy()
            scenario_metrics.update(scenario_params.get('adjustments', {}))
            
            # Run predictions for each model
            scenario_results = {
                'description': scenario_params.get('description', ''),
                'assumptions': scenario_params.get('assumptions', {}),
                'predictions': {}
            }
            
            # NPF prediction under scenario
            if 'gdp_growth' in scenario_params:
                scenario_data = pd.DataFrame({
                    'npf': [scenario_metrics['npf']],
                    'gdp_growth': [scenario_params['gdp_growth']],
                    'bi_rate': [scenario_params.get('bi_rate', 5.5)]
                }, index=[pd.Timestamp.now()])
                
                npf_forecast = self.models['npf'].predict(scenario_data, horizon=12)
                scenario_results['predictions']['npf'] = npf_forecast
                
            # Profitability under scenario
            profit_forecast = self.models['profitability'].predict_profitability(
                scenario_metrics,
                horizon=4
            )
            scenario_results['predictions']['profitability'] = profit_forecast
            
            # CAR trajectory under scenario
            car_forecast = self.models['car'].predict_car_trajectory(
                current_car=scenario_metrics['car'],
                current_npf=scenario_metrics['npf'],
                profit_forecast=profit_forecast['roa_forecast'],
                asset_growth_rate=scenario_params.get('asset_growth', 0.09)
            )
            scenario_results['predictions']['car'] = car_forecast
            
            # Overall health score for scenario
            scenario_results['health_score'] = self._calculate_scenario_score(
                scenario_results['predictions']
            )
            
            results[scenario_name] = scenario_results
            
        # Rank scenarios
        ranked_scenarios = self._rank_scenarios(results)
        
        return {
            'scenario_results': results,
            'scenario_ranking': ranked_scenarios,
            'recommended_scenario': ranked_scenarios[0] if ranked_scenarios else None,
            'key_insights': self._generate_scenario_insights(results)
        }
        
    def _calculate_scenario_score(self, predictions: Dict[str, Any]) -> float:
        """Calculate overall health score for scenario"""
        score = 50.0  # Base score
        
        # NPF impact
        if 'npf' in predictions:
            final_npf = predictions['npf']['forecast'].iloc[-1]
            if final_npf < 3:
                score += 20
            elif final_npf < 5:
                score += 10
            else:
                score -= 10
                
        # Profitability impact
        if 'profitability' in predictions:
            avg_roa = np.mean(predictions['profitability']['roa_forecast'])
            score += min(20, avg_roa * 10)
            
        # CAR impact
        if 'car' in predictions:
            min_car = predictions['car']['minimum_car']
            if min_car > 15:
                score += 20
            elif min_car > 12:
                score += 10
            else:
                score -= 20
                
        return min(100, max(0, score))
        
    def _rank_scenarios(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Rank scenarios by overall score"""
        ranked = []
        
        for name, data in results.items():
            ranked.append({
                'scenario': name,
                'score': data['health_score'],
                'key_metrics': {
                    'final_npf': data['predictions'].get('npf', {}).get('forecast', pd.Series()).iloc[-1] if 'npf' in data['predictions'] else None,
                    'avg_roa': np.mean(data['predictions'].get('profitability', {}).get('roa_forecast', [])) if 'profitability' in data['predictions'] else None,
                    'min_car': data['predictions'].get('car', {}).get('minimum_car', None)
                }
            })
            
        return sorted(ranked, key=lambda x: x['score'], reverse=True)
        
    def _generate_scenario_insights(self, results: Dict[str, Any]) -> List[str]:
        """Generate key insights from scenario analysis"""
        insights = []
        
        # Find best and worst scenarios
        scores = {name: data['health_score'] for name, data in results.items()}
        if scores:
            best_scenario = max(scores, key=scores.get)
            worst_scenario = min(scores, key=scores.get)
            
            insights.append(
                f"Best outcome under '{best_scenario}' scenario with score {scores[best_scenario]:.1f}"
            )
            insights.append(
                f"Highest risk under '{worst_scenario}' scenario with score {scores[worst_scenario]:.1f}"
            )
            
        # Common risks across scenarios
        insights.append(
            "NPF management remains critical across all scenarios"
        )
        insights.append(
            "Digital transformation essential for BOPO improvement"
        )
        
        return insights

def create_integrated_prediction_system() -> Dict[str, Any]:
    """
    Create an integrated prediction system combining all models
    """
    return {
        'npf_model': NPFPredictionModel(),
        'profitability_model': ProfitabilityPredictionModel(),
        'car_model': CARPredictionModel(),
        'customer_model': CustomerBehaviorModel(),
        'scenario_model': ScenarioAnalysisModel(),
        'description': 'Integrated prediction system for Bank Muamalat health monitoring'
    }