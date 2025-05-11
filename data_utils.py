"""
Utility functions for data processing and cleaning.
This module contains various helper functions for data manipulation and standardization.
"""

import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any, Tuple
import warnings


def standardize_column_names(df: pd.DataFrame, prefix: str = 'col') -> pd.DataFrame:
    """
    Standardize column names in a DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame whose columns need to be standardized
    prefix : str, optional (default='col')
        Prefix to add to column names that start with numbers
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with standardized column names
        
    Examples:
    --------
    >>> df = pd.DataFrame({'First Name': ['John'], '2nd Address': ['123 St']})
    >>> df_clean = standardize_column_names(df)
    >>> print(df_clean.columns.tolist())
    ['first_name', 'col_2nd_address']
    """
    def clean_column_name(col_name: str) -> str:
        # Convert to string and lowercase
        name = str(col_name).lower().strip()
        
        # Replace special characters and spaces with underscore
        name = re.sub(r'[^a-z0-9]', '_', name)
        
        # Remove duplicate underscores
        name = re.sub(r'_+', '_', name)
        
        # Remove leading and trailing underscores
        name = name.strip('_')
        
        # Ensure the name starts with a letter
        if not name[0].isalpha():
            name = f"{prefix}_{name}"
            
        return name
    
    # Create a dictionary of old and new column names
    new_columns = {col: clean_column_name(col) for col in df.columns}
    
    # Handle duplicate column names by adding a suffix
    seen = {}
    for old_col, new_col in new_columns.items():
        if new_col in seen:
            counter = seen[new_col]
            seen[new_col] += 1
            new_columns[old_col] = f"{new_col}_{counter}"
        else:
            seen[new_col] = 1
    
    # Create a new DataFrame with standardized column names
    df_standardized = df.rename(columns=new_columns)
    
    # Print the changes made
    print("Column name changes:")
    for old, new in new_columns.items():
        if old != new:
            print(f"{old:30} -> {new}")
    
    return df_standardized
    

def analyze_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze missing values in the DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame to analyze
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with missing value statistics
    """
    # Calculate missing value statistics
    missing_stats = pd.DataFrame({
        'missing_count': df.isnull().sum(),
        'missing_percentage': (df.isnull().sum() / len(df)) * 100,
        'dtype': df.dtypes
    })
    
    # Sort by missing percentage
    missing_stats = missing_stats.sort_values('missing_percentage', ascending=False)
    
    return missing_stats


def analyze_numeric_columns(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, plt.Figure]]:
    """
    Analyze numeric columns in the DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame to analyze
        
    Returns:
    --------
    Tuple[pandas.DataFrame, Dict[str, plt.Figure]]
        DataFrame with numeric statistics and dictionary of distribution plots
    """
    # Select numeric columns
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    
    # Calculate statistics
    stats = df[numeric_cols].describe()
    stats.loc['skew'] = df[numeric_cols].skew()
    stats.loc['kurtosis'] = df[numeric_cols].kurtosis()
    
    # Create distribution plots
    plots = {}
    for col in numeric_cols:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Histogram
        sns.histplot(data=df, x=col, ax=ax1)
        ax1.set_title(f'Distribution of {col}')
        
        # Box plot
        sns.boxplot(data=df, y=col, ax=ax2)
        ax2.set_title(f'Box Plot of {col}')
        
        plots[col] = fig
        plt.close(fig)
    
    return stats, plots


def analyze_categorical_columns(df: pd.DataFrame, max_categories: int = 20) -> Tuple[Dict[str, pd.Series], Dict[str, plt.Figure]]:
    """
    Analyze categorical columns in the DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame to analyze
    max_categories : int, optional (default=20)
        Maximum number of categories to display in plots
        
    Returns:
    --------
    Tuple[Dict[str, pd.Series], Dict[str, plt.Figure]]
        Dictionary of value counts and dictionary of bar plots
    """
    # Select categorical and boolean columns
    cat_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns
    
    value_counts = {}
    plots = {}
    
    for col in cat_cols:
        # Calculate value counts
        vc = df[col].value_counts()
        value_counts[col] = vc
        
        # Create bar plot
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if len(vc) > max_categories:
            # Show top categories and group others
            top_categories = vc.nlargest(max_categories)
            others = pd.Series({'Others': vc[max_categories:].sum()})
            vc_plot = pd.concat([top_categories, others])
        else:
            vc_plot = vc
            
        sns.barplot(x=vc_plot.index, y=vc_plot.values, ax=ax)
        ax.set_title(f'Distribution of {col}')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        
        plots[col] = fig
        plt.close(fig)
    
    return value_counts, plots


def analyze_correlations(df: pd.DataFrame) -> Tuple[pd.DataFrame, plt.Figure]:
    """
    Analyze correlations between numeric columns.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame to analyze
        
    Returns:
    --------
    Tuple[pandas.DataFrame, plt.Figure]
        Correlation matrix and heatmap plot
    """
    # Select numeric columns
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    
    # Calculate correlations
    corr_matrix = df[numeric_cols].corr()
    
    # Create correlation heatmap
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax)
    ax.set_title('Correlation Matrix')
    
    return corr_matrix, fig


def detect_outliers(df: pd.DataFrame, threshold: float = 1.5) -> Dict[str, pd.Series]:
    """
    Detect outliers in numeric columns using IQR method.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame to analyze
    threshold : float, optional (default=1.5)
        IQR multiplier for outlier detection
        
    Returns:
    --------
    Dict[str, pd.Series]
        Dictionary with outlier indices for each numeric column
    """
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    outliers = {}
    
    for col in numeric_cols:
        # Calculate IQR
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        # Define outlier bounds
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        
        # Find outliers
        outliers[col] = df[
            (df[col] < lower_bound) | 
            (df[col] > upper_bound)
        ][col]
    
    return outliers


def generate_summary_report(df: pd.DataFrame) -> str:
    """
    Generate a text summary report of the DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame to analyze
        
    Returns:
    --------
    str
        Summary report text
    """
    report = []
    
    # Basic information
    report.append("=== DATASET SUMMARY ===")
    report.append(f"Number of rows: {len(df)}")
    report.append(f"Number of columns: {len(df.columns)}")
    
    # Column types
    type_counts = df.dtypes.value_counts()
    report.append("\n=== COLUMN TYPES ===")
    for dtype, count in type_counts.items():
        report.append(f"{dtype}: {count} columns")
    
    # Memory usage
    memory_usage = df.memory_usage(deep=True).sum() / 1024**2  # Convert to MB
    report.append(f"\nMemory Usage: {memory_usage:.2f} MB")
    
    # Sample of column names by type
    report.append("\n=== COLUMNS BY TYPE ===")
    for dtype in type_counts.index:
        cols = df.select_dtypes(include=[dtype]).columns
        report.append(f"\n{dtype}:")
        report.append(", ".join(cols[:5]))
        if len(cols) > 5:
            report.append(f"... and {len(cols)-5} more")
    
    return "\n".join(report)


# Add more utility functions here as needed 