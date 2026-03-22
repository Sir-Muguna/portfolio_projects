from flask import Flask, jsonify, request
from flask_cors import CORS
from app.generators import AmazonDataGenerator
import os

app = Flask(__name__)
CORS(app)

# Initialize data generator
data_generator = AmazonDataGenerator()

# In-memory storage for generated data
data_store = {
    'master_sheet': None,  # pandas.DataFrame
    'daily_data': []       # list[dict]
}


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Amazon Seller Data API',
        'version': '1.0.0'
    })


@app.route('/api/generate-master', methods=['POST'])
def generate_master():
    """Generate the master sheet with N products (default 2500)"""
    try:
        num_entries = request.args.get('entries', 2500, type=int)
        master_sheet = data_generator.generate_master_sheet(num_entries)
        data_store['master_sheet'] = master_sheet
        return jsonify({
            'message': 'Master sheet generated successfully',
            'count': len(master_sheet),
            'sample': master_sheet.head(3).to_dict('records')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/daily-data', methods=['GET', 'POST'])
def daily_data():
    """Get or generate daily data"""
    if request.method == 'POST':
        if data_store['master_sheet'] is None:
            return jsonify({'error': 'Master sheet not generated yet'}), 400

        num_entries = request.args.get('entries', 100, type=int)
        try:
            daily_entries = data_generator.generate_daily_data(
                data_store['master_sheet'],
                num_entries
            )
            # Ensure extend works (list of dicts)
            if not isinstance(daily_entries, list):
                daily_entries = daily_entries.to_dict('records')

            data_store['daily_data'].extend(daily_entries)
            return jsonify({
                'message': f'Generated {len(daily_entries)} daily entries',
                'count': len(daily_entries),
                'data': daily_entries
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # GET
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page

    paginated_data = data_store['daily_data'][start_idx:end_idx]

    return jsonify({
        'page': page,
        'per_page': per_page,
        'total': len(data_store['daily_data']),
        'data': paginated_data
    })


@app.route('/api/master-sheet', methods=['GET'])
def get_master_sheet():
    """Get the master sheet data"""
    if data_store['master_sheet'] is None:
        return jsonify({'error': 'Master sheet not generated yet'}), 404

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    master_df = data_store['master_sheet']
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page

    data = master_df.iloc[start_idx:end_idx].to_dict('records')

    return jsonify({
        'page': page,
        'per_page': per_page,
        'total': len(master_df),
        'data': data
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() in ['1', 'true', 'yes']
    app.run(host='0.0.0.0', port=port, debug=debug)
