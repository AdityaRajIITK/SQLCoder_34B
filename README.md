# SQLCoder 34B - macOS Compatible

A macOS-compatible implementation of SQLCoder for generating SQL queries from natural language using the Llama-3-SQLCoder-8B model.

## Features

- 🔧 **macOS Compatible**: Fixed CUDA dependencies and bitsandbytes issues for Apple Silicon
- 🧠 **AI-Powered SQL Generation**: Uses Llama-3-SQLCoder-8B for accurate SQL query generation
- 📝 **Jupyter Notebook Interface**: Easy-to-use notebook environment
- 🚀 **Cross-Platform Device Detection**: Automatically detects and uses MPS (Apple Silicon), CUDA, or CPU

## Setup

### Prerequisites

- Python 3.8+
- macOS (tested on Apple Silicon)

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd SQLCoder\ 34B
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install additional dependency for macOS:
```bash
pip install psutil
```

## Usage

1. Activate your virtual environment:
```bash
source venv/bin/activate
```

2. Start Jupyter notebook:
```bash
jupyter notebook defog_sqlcoder_colab.ipynb
```

3. Run the cells in order to:
   - Load the model (automatically detects your device)
   - Generate SQL queries from natural language questions

### Example

```python
question = "What are the top 5 products by total sales quantity?"
generated_sql = generate_query(question)
print(generated_sql)
```

## macOS Compatibility Fixes

This version includes several fixes for macOS compatibility:

- ✅ Replaced CUDA memory detection with cross-platform device detection
- ✅ Removed bitsandbytes 4-bit quantization (not compatible with macOS)
- ✅ Added MPS (Apple Silicon) support
- ✅ Fixed device mapping for non-CUDA environments

## Database Schema

The model is configured with a sample e-commerce database schema including:
- Products
- Customers  
- Sales
- Salespeople
- Product Suppliers

You can modify the schema in the notebook to match your own database structure.

## Requirements

See `requirements.txt` for the complete list of dependencies.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on macOS
5. Submit a pull request

## License

This project is based on the original SQLCoder from Defog and adapted for macOS compatibility.

## Troubleshooting

### Common Issues

**Model Loading Errors**: If you encounter memory issues, the notebook will automatically use CPU offloading.

**Device Detection**: The notebook automatically detects the best available device (MPS > CUDA > CPU).

**Memory Management**: For Apple Silicon Macs, the system uses available RAM as an approximation for model loading decisions. 