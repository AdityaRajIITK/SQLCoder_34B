import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import re
from IPython.display import display

def create_visualization_from_nl(natural_language_query, result_df):
    """
    Simple natural language to visualization function.
    
    Args:
        natural_language_query: Natural language description of desired visualization
        result_df: Pandas DataFrame with the data to visualize
    """
    
    if result_df.empty:
        print("No data to visualize")
        return
    
    query_lower = natural_language_query.lower()
    
    # Convert potential datetime columns
    for col in result_df.columns:
        if result_df[col].dtype == 'object':
            # Try to convert to datetime if it looks like a date
            if any(keyword in col.lower() for keyword in ['date', 'time', 'created', 'day']):
                try:
                    result_df[col] = pd.to_datetime(result_df[col])
                    print(f"Converted {col} to datetime")
                except:
                    pass
    
    # Get column names and types
    numeric_cols = result_df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = result_df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = result_df.select_dtypes(include=['datetime64']).columns.tolist()
    
    print(f"Available columns:")
    print(f"  Numeric: {numeric_cols}")
    print(f"  Categorical: {categorical_cols}")
    print(f"  DateTime: {datetime_cols}")
    print()
    
    # Define a function to safely render Plotly charts
    def safe_plotly_show(fig, title):
        """Safely display Plotly chart with fallback options"""
        try:
            # Try normal display first
            fig.show()
            print(f"✅ Plotly {title} created successfully!")
            return True
        except Exception as e:
            print(f"⚠️  Plotly rendering issue: {str(e)}")
            
            # Try alternative rendering methods
            try:
                # Method 1: Try to render to HTML and show
                import tempfile
                import webbrowser
                
                with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                    fig.write_html(f.name)
                    print(f"📊 Chart saved to {f.name} - you can open it in your browser")
                return True
                
            except Exception as e2:
                print(f"⚠️  HTML rendering also failed: {str(e2)}")
                
                # Method 2: Show chart data instead
                try:
                    print("📋 Showing data instead:")
                    display(result_df.head(10))
                    return False
                except:
                    print("❌ Unable to display chart or data")
                    return False
    
    # Simple pattern matching for visualization types
    try:
        if any(word in query_lower for word in ['bar', 'column', 'count']):
            # Bar chart
            print("Creating bar chart...")
            
            # Determine x and y columns
            x_col = None
            y_col = None
            
            if len(datetime_cols) >= 1 and len(numeric_cols) >= 1:
                x_col = datetime_cols[0]
                y_col = numeric_cols[0]
            elif len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
                x_col = categorical_cols[0]
                y_col = numeric_cols[0]
            elif len(result_df.columns) >= 2:
                x_col = result_df.columns[0]
                y_col = result_df.columns[1]
            
            if x_col and y_col:
                # Create with Plotly
                fig = px.bar(result_df, x=x_col, y=y_col, 
                           title=f'Bar Chart: {y_col} by {x_col}')
                fig.update_layout(
                    xaxis_title=x_col,
                    yaxis_title=y_col,
                    showlegend=False
                )
                
                # Try to show Plotly chart
                plotly_success = safe_plotly_show(fig, "bar chart")
                
                # Always create Matplotlib version as backup
                print("\n📊 Creating Matplotlib backup chart...")
                try:
                    plt.figure(figsize=(12, 6))
                    if len(result_df) > 20:  # If too many bars, rotate labels
                        plt.xticks(rotation=45)
                    
                    sns.barplot(data=result_df, x=x_col, y=y_col)
                    plt.title(f'Bar Chart: {y_col} by {x_col}')
                    plt.xlabel(x_col)
                    plt.ylabel(y_col)
                    plt.tight_layout()
                    plt.show()
                    
                    print(f"✅ Matplotlib bar chart created with {x_col} vs {y_col}")
                except Exception as e:
                    print(f"❌ Matplotlib chart also failed: {e}")
                    display(result_df.head(10))
                
                return
                
        elif any(word in query_lower for word in ['line', 'trend', 'time', 'over time']):
            # Line chart
            print("Creating line chart...")
            
            x_col = None
            y_col = None
            
            if len(datetime_cols) >= 1 and len(numeric_cols) >= 1:
                x_col = datetime_cols[0]
                y_col = numeric_cols[0]
            elif len(result_df.columns) >= 2:
                x_col = result_df.columns[0]
                y_col = result_df.columns[1]
            
            if x_col and y_col:
                # Create with Plotly
                fig = px.line(result_df, x=x_col, y=y_col,
                             title=f'Line Chart: {y_col} over {x_col}',
                             markers=True)
                
                # Try to show Plotly chart
                plotly_success = safe_plotly_show(fig, "line chart")
                
                # Create Matplotlib version as backup
                print("\n📊 Creating Matplotlib backup chart...")
                try:
                    plt.figure(figsize=(12, 6))
                    plt.plot(result_df[x_col], result_df[y_col], marker='o', linewidth=2, markersize=4)
                    plt.title(f'Line Chart: {y_col} over {x_col}')
                    plt.xlabel(x_col)
                    plt.ylabel(y_col)
                    plt.xticks(rotation=45)
                    plt.grid(True, alpha=0.3)
                    plt.tight_layout()
                    plt.show()
                    
                    print(f"✅ Matplotlib line chart created with {x_col} vs {y_col}")
                except Exception as e:
                    print(f"❌ Matplotlib chart also failed: {e}")
                    display(result_df.head(10))
                
                return
                
        elif any(word in query_lower for word in ['scatter', 'correlation', 'relationship']):
            # Scatter plot
            print("Creating scatter plot...")
            if len(numeric_cols) >= 2:
                x_col = numeric_cols[0]
                y_col = numeric_cols[1]
                
                # Create with Plotly
                fig = px.scatter(result_df, x=x_col, y=y_col,
                               title=f'Scatter Plot: {y_col} vs {x_col}')
                
                plotly_success = safe_plotly_show(fig, "scatter plot")
                
                if not plotly_success:
                    # Matplotlib fallback
                    try:
                        plt.figure(figsize=(10, 6))
                        plt.scatter(result_df[x_col], result_df[y_col], alpha=0.6)
                        plt.title(f'Scatter Plot: {y_col} vs {x_col}')
                        plt.xlabel(x_col)
                        plt.ylabel(y_col)
                        plt.show()
                        print(f"✅ Matplotlib scatter plot created with {x_col} vs {y_col}")
                    except Exception as e:
                        print(f"❌ Matplotlib chart also failed: {e}")
                        display(result_df.head(10))
                return
                
        elif any(word in query_lower for word in ['pie', 'distribution', 'proportion']):
            # Pie chart
            print("Creating pie chart...")
            if len(categorical_cols) >= 1:
                col = categorical_cols[0]
                value_counts = result_df[col].value_counts()
                
                # Create with Plotly
                fig = px.pie(values=value_counts.values, names=value_counts.index,
                           title=f'Distribution of {col}')
                
                plotly_success = safe_plotly_show(fig, "pie chart")
                
                if not plotly_success:
                    # Matplotlib fallback
                    try:
                        plt.figure(figsize=(8, 8))
                        plt.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
                        plt.title(f'Distribution of {col}')
                        plt.show()
                        print(f"✅ Matplotlib pie chart created for {col}")
                    except Exception as e:
                        print(f"❌ Matplotlib chart also failed: {e}")
                        display(result_df.head(10))
                        
                return
                
        elif any(word in query_lower for word in ['histogram', 'frequency']):
            # Histogram
            print("Creating histogram...")
            if len(numeric_cols) >= 1:
                col = numeric_cols[0]
                
                # Create with Plotly
                fig = px.histogram(result_df, x=col,
                                 title=f'Histogram of {col}')
                
                plotly_success = safe_plotly_show(fig, "histogram")
                
                if not plotly_success:
                    # Matplotlib fallback
                    try:
                        plt.figure(figsize=(10, 6))
                        plt.hist(result_df[col], bins=20, alpha=0.7)
                        plt.title(f'Histogram of {col}')
                        plt.xlabel(col)
                        plt.ylabel('Frequency')
                        plt.show()
                        print(f"✅ Matplotlib histogram created for {col}")
                    except Exception as e:
                        print(f"❌ Matplotlib chart also failed: {e}")
                        display(result_df.head(10))
                        
                return
                
        elif any(word in query_lower for word in ['heatmap', 'correlation matrix']):
            # Heatmap (correlation matrix)
            print("Creating heatmap...")
            if len(numeric_cols) >= 2:
                corr_matrix = result_df[numeric_cols].corr()
                
                # Always use matplotlib for heatmaps as it's more reliable
                try:
                    plt.figure(figsize=(10, 8))
                    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
                    plt.title('Correlation Heatmap')
                    plt.tight_layout()
                    plt.show()
                    
                    print(f"✅ Correlation heatmap created")
                except Exception as e:
                    print(f"❌ Heatmap creation failed: {e}")
                    display(corr_matrix)
                return
        
        # If no specific pattern matched, try to create a sensible default
        print("No specific visualization pattern detected. Creating default visualization...")
        
        if len(datetime_cols) >= 1 and len(numeric_cols) >= 1:
            # Default to line chart for time series data
            x_col = datetime_cols[0]
            y_col = numeric_cols[0]
            
            fig = px.line(result_df, x=x_col, y=y_col,
                         title=f'Line Chart: {y_col} over {x_col}',
                         markers=True)
            
            plotly_success = safe_plotly_show(fig, "default line chart")
            
            # Matplotlib backup
            try:
                plt.figure(figsize=(12, 6))
                plt.plot(result_df[x_col], result_df[y_col], marker='o', linewidth=2)
                plt.title(f'{y_col} over {x_col}')
                plt.xlabel(x_col)
                plt.ylabel(y_col)
                plt.xticks(rotation=45)
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.show()
                
                print(f"✅ Default line chart created with {x_col} vs {y_col}")
            except Exception as e:
                print(f"❌ Backup chart failed: {e}")
                display(result_df.head(10))
            
        elif len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
            # Default to bar chart for categorical data
            x_col = categorical_cols[0]
            y_col = numeric_cols[0]
            
            fig = px.bar(result_df, x=x_col, y=y_col,
                        title=f'Bar Chart: {y_col} by {x_col}')
            
            plotly_success = safe_plotly_show(fig, "default bar chart")
            
            # Matplotlib backup
            try:
                plt.figure(figsize=(10, 6))
                sns.barplot(data=result_df, x=x_col, y=y_col)
                plt.title(f'{y_col} by {x_col}')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
                
                print(f"✅ Default bar chart created with {x_col} vs {y_col}")
            except Exception as e:
                print(f"❌ Backup chart failed: {e}")
                display(result_df.head(10))
            
        else:
            # Show data table and suggestions
            print("Here's your data:")
            display(result_df.head(10))
            
            print("\nSuggested visualizations based on your data:")
            if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
                print("- Try: 'Create a bar chart'")
            if len(numeric_cols) >= 2:
                print("- Try: 'Create a scatter plot'")
                print("- Try: 'Show correlation heatmap'")
            if len(datetime_cols) >= 1:
                print("- Try: 'Create a line chart over time'")
            if len(categorical_cols) >= 1:
                print("- Try: 'Create a pie chart'")
            if len(numeric_cols) >= 1:
                print("- Try: 'Create a histogram'")
                
    except Exception as e:
        print(f"❌ Error creating visualization: {e}")
        print("\nShowing data table instead:")
        display(result_df.head(10))

def query_and_visualize(question, visualization_request, engine, generate_query_func):
    """
    Combined function to query database and create visualization
    
    Args:
        question: SQL question for the model
        visualization_request: Natural language description of desired visualization
        engine: Database engine
        generate_query_func: Function to generate SQL queries
    """
    print(f"Question: {question}\n")
    
    # Generate SQL query
    sql_query = generate_query_func(question)
    print("Generated SQL Query:")
    print(sql_query)
    print("\n" + "="*50 + "\n")
    
    try:
        # Execute query
        result_df = pd.read_sql_query(sql_query, engine)
        print(f"Query returned {len(result_df)} rows.\n")
        
        # Create visualization
        print(f"Creating visualization: {visualization_request}\n")
        create_visualization_from_nl(visualization_request, result_df)
        
    except Exception as e:
        print(f"Error executing query: {e}")

def show_visualization_examples():
    """
    Show examples of how to use the visualization functions
    """
    print("🎨 Natural Language to Visualization Examples:")
    print("=" * 50)
    print()
    print("1. Basic usage with existing DataFrame:")
    print("   create_visualization_from_nl('Create a bar chart', your_dataframe)")
    print()
    print("2. Query and visualize in one step:")
    print("   query_and_visualize(")
    print("       question='Show node count by day',")
    print("       visualization_request='Create a line chart',")
    print("       engine=db_engine,")
    print("       generate_query_func=generate_query")
    print("   )")
    print()
    print("3. Supported visualization types:")
    print("   - Bar charts: 'Create a bar chart', 'Show me a column chart'")
    print("   - Line charts: 'Create a line chart', 'Show trend over time'")
    print("   - Scatter plots: 'Create a scatter plot', 'Show correlation'")
    print("   - Pie charts: 'Create a pie chart', 'Show distribution'")
    print("   - Histograms: 'Create a histogram', 'Show frequency'")
    print("   - Heatmaps: 'Show correlation heatmap', 'Create a heatmap'")
    print()
    print("💡 The function will automatically detect column types and suggest")
    print("   appropriate visualizations if your request is not recognized.")
    print()
    print("🔧 Error Handling:")
    print("   - Automatically falls back to Matplotlib if Plotly fails")
    print("   - Shows data tables if charts can't be rendered")
    print("   - Provides helpful suggestions based on your data")

def quick_visualize(sql_query, visualization_request, engine):
    """
    Quick function to execute SQL and create visualization in one step
    
    Args:
        sql_query: SQL query string
        visualization_request: Natural language description of desired visualization
        engine: Database engine
    """
    try:
        # Execute query
        result_df = pd.read_sql_query(sql_query, engine)
        print(f"Query returned {len(result_df)} rows.\n")
        
        # Create visualization
        print(f"Creating visualization: {visualization_request}\n")
        create_visualization_from_nl(visualization_request, result_df)
        
    except Exception as e:
        print(f"Error executing query: {e}")

if __name__ == "__main__":
    show_visualization_examples() 