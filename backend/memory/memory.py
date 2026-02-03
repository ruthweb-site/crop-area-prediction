"""
Memory Layer - Stores predictions, queries, and enables learning from past data.
"""
import json
import os
import aiosqlite
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

class MemoryLayer:
    """
    Persistent memory storage for CropAgent.
    
    Stores:
    - Prediction history
    - User queries
    - Agent performance metrics
    - Learning data for improvements
    """
    
    def __init__(self, db_path: str = "cropagent.db"):
        self.db_path = db_path
        self._initialized = False
    
    async def initialize(self):
        """Initialize the database with required tables."""
        if self._initialized:
            return
            
        async with aiosqlite.connect(self.db_path) as db:
            # Predictions table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    state TEXT NOT NULL,
                    crop TEXT NOT NULL,
                    predicted_yield REAL,
                    risk_score REAL,
                    confidence INTEGER,
                    weather_data TEXT,
                    soil_data TEXT,
                    satellite_data TEXT,
                    full_response TEXT
                )
            ''')
            
            # User queries table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    query TEXT NOT NULL,
                    language TEXT,
                    state TEXT,
                    crop TEXT,
                    response_time_ms INTEGER
                )
            ''')
            
            # Agent metrics table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS agent_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    agent_name TEXT NOT NULL,
                    execution_time_ms INTEGER,
                    success INTEGER,
                    error_message TEXT
                )
            ''')
            
            # Alerts history
            await db.execute('''
                CREATE TABLE IF NOT EXISTS alerts_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    state TEXT NOT NULL,
                    alert_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    message TEXT,
                    was_accurate INTEGER DEFAULT NULL
                )
            ''')
            
            await db.commit()
            self._initialized = True
    
    async def store_prediction(self, prediction_data: Dict[str, Any]) -> int:
        """Store a prediction in the database."""
        await self.initialize()
        
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
                INSERT INTO predictions 
                (timestamp, state, crop, predicted_yield, risk_score, confidence,
                 weather_data, soil_data, satellite_data, full_response)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                prediction_data.get("state", ""),
                prediction_data.get("crop", ""),
                prediction_data.get("predicted_yield", 0),
                prediction_data.get("risk_score", 0),
                prediction_data.get("confidence", 0),
                json.dumps(prediction_data.get("weather_data", {})),
                json.dumps(prediction_data.get("soil_data", {})),
                json.dumps(prediction_data.get("satellite_data", {})),
                json.dumps(prediction_data.get("full_response", {}))
            ))
            await db.commit()
            return cursor.lastrowid
    
    async def store_query(self, query_data: Dict[str, Any]) -> int:
        """Store a user query."""
        await self.initialize()
        
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
                INSERT INTO queries (timestamp, query, language, state, crop, response_time_ms)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                query_data.get("query", ""),
                query_data.get("language", "en"),
                query_data.get("state", ""),
                query_data.get("crop", ""),
                query_data.get("response_time_ms", 0)
            ))
            await db.commit()
            return cursor.lastrowid
    
    async def store_agent_metric(self, agent_name: str, execution_time_ms: int, 
                                  success: bool, error_message: str = None):
        """Store agent performance metrics."""
        await self.initialize()
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT INTO agent_metrics (timestamp, agent_name, execution_time_ms, success, error_message)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                agent_name,
                execution_time_ms,
                1 if success else 0,
                error_message
            ))
            await db.commit()
    
    async def store_alert(self, state: str, alert_type: str, severity: str, message: str):
        """Store an alert in history."""
        await self.initialize()
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT INTO alerts_history (timestamp, state, alert_type, severity, message)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                state,
                alert_type,
                severity,
                message
            ))
            await db.commit()
    
    async def get_recent_predictions(self, state: str = None, crop: str = None, 
                                      limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent predictions, optionally filtered by state/crop."""
        await self.initialize()
        
        query = "SELECT * FROM predictions"
        params = []
        conditions = []
        
        if state:
            conditions.append("state = ?")
            params.append(state)
        if crop:
            conditions.append("crop = ?")
            params.append(crop)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
    
    async def get_historical_yields(self, state: str, crop: str, 
                                     days: int = 365) -> List[Dict[str, Any]]:
        """Get historical yield predictions for trend analysis."""
        await self.initialize()
        
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('''
                SELECT timestamp, predicted_yield, risk_score, confidence
                FROM predictions
                WHERE state = ? AND crop = ? AND timestamp > ?
                ORDER BY timestamp ASC
            ''', (state, crop, cutoff_date)) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
    
    async def get_query_statistics(self) -> Dict[str, Any]:
        """Get query statistics for analytics."""
        await self.initialize()
        
        async with aiosqlite.connect(self.db_path) as db:
            # Total queries
            async with db.execute("SELECT COUNT(*) FROM queries") as cursor:
                total = (await cursor.fetchone())[0]
            
            # Queries by language
            async with db.execute('''
                SELECT language, COUNT(*) as count 
                FROM queries 
                GROUP BY language
            ''') as cursor:
                by_language = {row[0]: row[1] for row in await cursor.fetchall()}
            
            # Most queried states
            async with db.execute('''
                SELECT state, COUNT(*) as count 
                FROM queries 
                WHERE state IS NOT NULL
                GROUP BY state 
                ORDER BY count DESC 
                LIMIT 5
            ''') as cursor:
                top_states = {row[0]: row[1] for row in await cursor.fetchall()}
            
            # Most queried crops
            async with db.execute('''
                SELECT crop, COUNT(*) as count 
                FROM queries 
                WHERE crop IS NOT NULL
                GROUP BY crop 
                ORDER BY count DESC 
                LIMIT 5
            ''') as cursor:
                top_crops = {row[0]: row[1] for row in await cursor.fetchall()}
            
            return {
                "total_queries": total,
                "by_language": by_language,
                "top_states": top_states,
                "top_crops": top_crops
            }
    
    async def get_agent_performance(self) -> Dict[str, Any]:
        """Get agent performance metrics."""
        await self.initialize()
        
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('''
                SELECT 
                    agent_name,
                    COUNT(*) as total_executions,
                    AVG(execution_time_ms) as avg_time_ms,
                    SUM(success) as successful,
                    COUNT(*) - SUM(success) as failed
                FROM agent_metrics
                GROUP BY agent_name
            ''') as cursor:
                rows = await cursor.fetchall()
                
                return {
                    row[0]: {
                        "total_executions": row[1],
                        "avg_time_ms": round(row[2] or 0, 2),
                        "successful": row[3],
                        "failed": row[4],
                        "success_rate": round(row[3] / row[1] * 100, 1) if row[1] > 0 else 0
                    }
                    for row in rows
                }
    
    async def learn_from_feedback(self, prediction_id: int, actual_yield: float):
        """
        Store actual yield data for learning.
        This can be used to improve prediction accuracy over time.
        """
        await self.initialize()
        
        # Get the original prediction
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT predicted_yield FROM predictions WHERE id = ?", 
                (prediction_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    predicted = row["predicted_yield"]
                    error = actual_yield - predicted
                    error_percentage = (error / predicted * 100) if predicted > 0 else 0
                    
                    # Store feedback (could be enhanced with a separate feedback table)
                    # For now, we just log it
                    print(f"Learning: Prediction {prediction_id} - "
                          f"Predicted: {predicted}, Actual: {actual_yield}, "
                          f"Error: {error_percentage:.1f}%")
    
    async def cleanup_old_data(self, days_to_keep: int = 365):
        """Remove data older than specified days."""
        await self.initialize()
        
        cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).isoformat()
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "DELETE FROM predictions WHERE timestamp < ?", 
                (cutoff_date,)
            )
            await db.execute(
                "DELETE FROM queries WHERE timestamp < ?", 
                (cutoff_date,)
            )
            await db.execute(
                "DELETE FROM agent_metrics WHERE timestamp < ?", 
                (cutoff_date,)
            )
            await db.commit()


# Global memory instance
memory = MemoryLayer()
