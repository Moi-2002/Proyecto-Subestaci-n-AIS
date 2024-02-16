from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    if request.method == 'POST':
        ##Tensiones representativas (Urp)##
        #-Tensión a frecuencia industrial-#
        Un = float(request.form['num1'])
        Us = float(request.form['num2'])
        Um = Us
        Ubase = np.round(Us * np.sqrt(2) / np.sqrt(3))


        # -Sobretensiones temporales- #
        # ...Por falla a tierra... #
        K = float(request.form['num3'])
        Urp_ft = np.round(K * (Us / np.sqrt(3)))

        # ...Rechazo por carga... #
        K_rc = float(request.form['num4'])
        Urpff_rc = np.round(K_rc * (Us))
        if Urp_ft > Urpff_rc / np.sqrt(3):
            Urprc_rc = Urp_ft
        else:
             Urprc_rc = Urpff_rc / np.sqrt(3)       
        Urprc_rc = np.round(Urprc_rc)

        # -Sobretensiones de frente lento- #
        # ...Impulsos que afectan equipos de entrada de línea, energización en extremo remoto... #
        Ue2_ex = float(request.form['num5'])
        Uet_ex = np.round(1.25 * Ue2_ex - 0.25)
        Uet2_ex = np.round(Uet_ex * Ubase)
        Up2_ex = float(request.form['num6'])
        Uptex_pu = np.round(1.25 * Up2_ex - 0.43)
        Uptex_kv = np.round(Uptex_pu * Ubase)

        # ...Impulsos que afectan todos los equipos, energización en extremo local... #
        Ue2_el = float(request.form['num7'])
        Uet_el = np.round(1.25 * Ue2_el - 0.25)
        Uet2_el = np.round(Uet_el * Ubase)
        Up2_el =float(request.form['num8'])
        Uptel_pu = np.round(1.25 * Up2_el - 0.43)
        Uptel_kv = np.round(Uptel_pu * Ubase)

        # ...Impulsos que afectan todos los equipos, energización en extremo local... #
        NPM = float(request.form['num9'])
        NPR = float(request.form['num10'])
        Urp_ce = np.minimum(NPM, Uet2_el )
        if (2 * NPM) < Uptel_kv:
         Urp_el = 2 * NPM
        else:
         Urp_el = Uptel_kv
        Urp_eel = Urp_el
    ######################################################################################

        ##Tensiones de soportabilidad para coordinación (UCW)##
        # -Sobretensiones temporales- #

            







        return  render_template('index.html', r1=Um, r2=Ubase, r3=Urp_ft, r4=Urpff_rc, r5=Urprc_rc,
                                 r6=Uet_ex, r7=Uet2_ex, r8=Uptex_pu, r9=Uptex_kv, r10=Uet_el,
                                 r11=Uet2_el, r12=Uptel_pu, r13=Uptel_kv, r14=Urp_ce,
                                 r15=Urp_el, r16=Urp_eel)


if __name__ == '__main__':
    app.run(debug=True)

