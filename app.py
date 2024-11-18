from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# Configure API key for GenAI
genai.configure(api_key="AIzaSyCLoM-OhRrz4ulIzOjHOlZur4LGlFlOdfI")

# Initialize the generative model
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)


def generate_pen_testing_guidance(phase, target_type, target_details, os):
    # Construct prompt based on selected phase, target type, and OS
    prompt = f"""
    You are conducting penetration testing on a {target_type} ({target_details}) during the {phase} phase. 
    The target machine is running {os}. Provide a detailed guide with the following:
    1. Step-by-step actions to take based on the target and phase.
    2. Tools/commands/scripts for the specified OS (Kali, Ubuntu, Windows, etc.).
    3. Justifications for the tools/scripts and alternatives in a table format.
    """

    try:
        # Use the model to generate the content
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating content: {e}"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    phase = data.get('phase')
    target_type = data.get('targetType')
    target_details = data.get('targetDetails')
    os = data.get('os')

    result = generate_pen_testing_guidance(phase, target_type, target_details, os)
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)
