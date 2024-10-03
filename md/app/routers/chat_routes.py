from flask import Blueprint, request, jsonify
from app.utils.code_utils import extract_code_and_text

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route('/api/generate', methods=['POST'])
def generate_code():
    data = request.json
    user_input = data.get('input', '')

    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    # For demonstration purposes, we return static content similar to the provided samples
    try:
        sample_response = {

  'role': 'assistant',
  'content': "In order to create an end-to-end model for time series forecasting, the following steps are crucial:\n\n```python\ndef time_series_model(data):\n    from sklearn.model_selection import train_test_split\n    from sklearn.preprocessing import StandardScaler\n    from keras.models import Sequential\n    from keras.layers import LSTM, Dense\n\n    # Preprocessing\n    scaler = StandardScaler()\n    data_scaled = scaler.fit_transform(data)\n\n    # Train/test split\n    train, test = train_test_split(data_scaled, test_size=0.2, shuffle=False)\n\n    # Model\n    model = Sequential()\n    model.add(LSTM(50, return_sequences=True, input_shape=(train.shape[1], 1)))\n    model.add(LSTM(50))\n    model.add(Dense(1))\n\n    model.compile(optimizer='adam', loss='mse')\n\n    model.fit(train, epochs=10, batch_size=32, validation_data=(test,))\n\n    return model\n```\nOnce the model is trained, it can be used to predict future time series data."

        }

        model_response = sample_response.get('content', '')

        # Extract code and text using the utility function
            # Extract code and text from the response
        response_parts = extract_code_and_text(model_response)

        return jsonify({"response": response_parts}), 200
    except Exception as e:
        print(f"Error: {e}")
    return jsonify({"error": "Error generating response"}), 500
