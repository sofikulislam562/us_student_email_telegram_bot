#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database module with modern connection handling
"""

import pymysql
from typing import Optional, List, Dict, Any
import logging
from contextlib import contextmanager
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Modern database connection handler with context manager support"""
    
    def __init__(self):
        self.host = DB_HOST
        self.port = DB_PORT
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.db = DB_NAME
    
    @contextmanager
    def get_connection(self):
        """Get database connection with context manager"""
        conn = None
        try:
            conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def add_user_detail(self, data: List[Any]) -> bool:
        """Add new user details to database"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = """INSERT INTO user_detail_our_email
                    (userName, fullName, gender, title, race, birthday, ssn, street, city, state, 
                     stateFull, zipCode, phoneNumber, mobileNumber, email, email_pwd, email_server, register_time) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql, data)
            logger.info(f"User added: {data[14]}")
            return True
        except Exception as e:
            logger.error(f"Failed to add user: {e}")
            return False
    
    def get_user_detail(self, tag: int) -> Optional[Dict[str, Any]]:
        """Get user detail by tag status"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = "SELECT * FROM user_detail_our_email WHERE tag=%s ORDER BY register_time LIMIT 1"
                    cursor.execute(sql, (tag,))
                    result = cursor.fetchone()
                    return result
        except Exception as e:
            logger.error(f"Failed to get user detail: {e}")
            return None
    
    def update_user_tag(self, email: str, tag: int) -> bool:
        """Update user status tag"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = "UPDATE user_detail_our_email SET tag=%s WHERE email=%s"
                    cursor.execute(sql, (tag, email))
            logger.info(f"User tag updated: {email} -> {tag}")
            return True
        except Exception as e:
            logger.error(f"Failed to update user tag: {e}")
            return False
    
    def add_email_detail(self, data: List[Any]) -> bool:
        """Add email details to database"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = "INSERT INTO email_detail (stu_id, edu_email, edu_pwd, collect_time, college_id) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, data)
            logger.info(f"Email detail added for: {data[1]}")
            return True
        except Exception as e:
            logger.error(f"Failed to add email detail: {e}")
            return False
    
    def delete_user_detail(self, email: str) -> bool:
        """Delete user detail by email"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = "DELETE FROM user_detail_our_email WHERE email=%s"
                    cursor.execute(sql, (email,))
            logger.info(f"User deleted: {email}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete user: {e}")
            return False
    
    def get_all_users_by_tag(self, tag: int, limit: int = 20) -> List[Dict[str, Any]]:
        """Get all users with specific tag"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = "SELECT * FROM user_detail_our_email WHERE tag=%s ORDER BY register_time DESC LIMIT %s"
                    cursor.execute(sql, (tag, limit))
                    results = cursor.fetchall()
                    return results if results else []
        except Exception as e:
            logger.error(f"Failed to get users by tag: {e}")
            return []
