from fastapi import APIRouter, Request
from app.utils.code_utils import extract_code_and_text
from fastapi.responses import JSONResponse

chat_bp = APIRouter()

@chat_bp.post('/api/generate')
async def generate_code(request: Request):
    try:
        data = await request.json()
        user_input = data.get('input', '')
        if not user_input:
            return JSONResponse({'error': 'No input provided'}), 400

    # For demonstration purposes, we return static content similar to the provided samples
        sample_response = {

  'role': 'assistant',
  'content': "In order to create an end-to-end model for time series forecasting, the following steps are crucial:\n\n```python\ndef time_series_model(data):\n    from sklearn.model_selection import train_test_split\n    from sklearn.preprocessing import StandardScaler\n    from keras.models import Sequential\n    from keras.layers import LSTM, Dense\n\n    # Preprocessing\n    scaler = StandardScaler()\n    data_scaled = scaler.fit_transform(data)\n\n    # Train/test split\n    train, test = train_test_split(data_scaled, test_size=0.2, shuffle=False)\n\n    # Model\n    model = Sequential()\n    model.add(LSTM(50, return_sequences=True, input_shape=(train.shape[1], 1)))\n    model.add(LSTM(50))\n    model.add(Dense(1))\n\n    model.compile(optimizer='adam', loss='mse')\n\n    model.fit(train, epochs=10, batch_size=32, validation_data=(test,))\n\n    return model\n```\nOnce the model is trained, it can be used to predict future time series data."

        }

        model_response = sample_response.get('content', '')

        # Extract code and text using the utility function
            # Extract code and text from the response
        response_parts = extract_code_and_text(model_response)

        return JSONResponse(content={"response": response_parts})
    except Exception as e:
        print(f"Error: {e}")
    return JSONResponse({"error": "Error generating response"}), 500
