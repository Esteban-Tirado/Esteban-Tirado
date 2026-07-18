from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

history = []

def calcular(expresion, modo='deg'):
    try:
        expr = expresion.strip()
        expr = expr.replace('^', '**')
        expr = expr.replace('×', '*')
        expr = expr.replace('÷', '/')
        expr = expr.replace('π', str(math.pi))
        expr = expr.replace('e', str(math.e))

        def sin_f(x): return math.sin(math.radians(x)) if modo == 'deg' else math.sin(x)
        def cos_f(x): return math.cos(math.radians(x)) if modo == 'deg' else math.cos(x)
        def tan_f(x): return math.tan(math.radians(x)) if modo == 'deg' else math.tan(x)
        def asin_f(x):
            r = math.asin(x)
            return math.degrees(r) if modo == 'deg' else r
        def acos_f(x):
            r = math.acos(x)
            return math.degrees(r) if modo == 'deg' else r
        def atan_f(x):
            r = math.atan(x)
            return math.degrees(r) if modo == 'deg' else r

        contexto = {
            '__builtins__': {},
            'sin': sin_f, 'cos': cos_f, 'tan': tan_f,
            'asin': asin_f, 'acos': acos_f, 'atan': atan_f,
            'ln': math.log, 'log': math.log10,
            'sqrt': math.sqrt, 'abs': abs,
            'factorial': math.factorial,
            'pi': math.pi, 'e': math.e,
            'exp': math.exp, 'pow': pow,
        }

        resultado = eval(expr, contexto)

        if isinstance(resultado, float):
            if resultado == int(resultado):
                resultado = int(resultado)
            else:
                resultado = round(resultado, 10)

        return str(resultado), None
    except ZeroDivisionError:
        return None, 'Error: División por cero'
    except Exception as ex:
        return None, f'Error: {str(ex)}'

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/calcular', methods=['POST'])
def calcular_route():
    data = request.get_json()
    expresion = data.get('expresion', '')
    modo = data.get('modo', 'deg')
    resultado, error = calcular(expresion, modo)
    if error:
        return jsonify({'error': error})
    history.append({'expresion': expresion, 'resultado': resultado})
    if len(history) > 20:
        history.pop(0)
    return jsonify({'resultado': resultado})

@app.route('/historial')
def historial():
    return jsonify({'historial': history[-10:][::-1]})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)