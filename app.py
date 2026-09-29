import gradio as gr
from geochemical_geothermometer import calculate_temperature, enthalpy_class

def compute(method, na, k, ca, sio2, beta_choice):
    # Build concentrations dict
    conc = {}
    if method in ["Na-K (Fournier, 1979)", "Na-K (Giggenbach, 1988)"]:
        if na is None or k is None:
            return "Please provide Na and K values."
        conc['Na'] = na
        conc['K'] = k
    elif method == "Na-K-Ca (Fournier & Truesdell, 1973)":
        if na is None or k is None or ca is None:
            return "Please provide Na, K and Ca values."
        conc['Na'] = na
        conc['K'] = k
        conc['Ca'] = ca
    elif method in ["Quartz (no steam loss)", "Quartz (adiabatic cooling)"]:
        if sio2 is None:
            return "Please provide SiO2 value."
        conc['SiO2'] = sio2
    else:
        return "Unknown method selected."

    # Validate all numeric inputs > 0
    for key, value in conc.items():
        if value <= 0:
            return f"All concentrations must be positive. {key} is {value}."

    try:
        # For Na-K-Ca, pass beta if selected
        if method == "Na-K-Ca (Fournier & Truesdell, 1973)":
            if beta_choice == "1/3":
                beta = 1/3
            elif beta_choice == "4/3":
                beta = 4/3
            else:  # Automatic (iterative)
                beta = None  # function will handle iterative
            temp = calculate_temperature(method, conc, beta)
        else:
            temp = calculate_temperature(method, conc)
    except ValueError as e:
        return str(e)

    classification = enthalpy_class(temp)
    formula_info = get_formula_text(method, conc)
    return f"Temperature: {temp:.1f} °C\nEnthalpy class: {classification}\nFormula: {formula_info}"

def get_formula_text(method, conc):
    if "Fournier" in method and "Na-K" in method:
        return "T = 1217 / (log10(Na/K) + 1.483) - 273.15"
    elif "Giggenbach" in method:
        return "T = 1390 / (log10(Na/K) + 1.750) - 273.15"
    elif "Na-K-Ca" in method:
        return "T = 1647 / (log10(Na/K) + β*log10(sqrt(Ca)/Na) + 2.24) - 273.15"
    elif "no steam loss" in method:
        return "T = 72.5*(log10(SiO2))^2 - 36.0*log10(SiO2) + 42.4"
    elif "adiabatic" in method:
        return "T = 42.2*(log10(SiO2))^2 - 22.0*log10(SiO2) + 24.4"
    return ""

def update_inputs(method):
    show_na_k = method in ["Na-K (Fournier, 1979)", "Na-K (Giggenbach, 1988)", "Na-K-Ca (Fournier & Truesdell, 1973)"]
    show_ca = method == "Na-K-Ca (Fournier & Truesdell, 1973)"
    show_sio2 = method in ["Quartz (no steam loss)", "Quartz (adiabatic cooling)"]
    show_beta = method == "Na-K-Ca (Fournier & Truesdell, 1973)"
    return {
        na_input: gr.update(visible=show_na_k, value=10 if show_na_k else None),
        k_input: gr.update(visible=show_na_k, value=1 if show_na_k else None),
        ca_input: gr.update(visible=show_ca, value=50 if show_ca else None),
        sio2_input: gr.update(visible=show_sio2, value=100 if show_sio2 else None),
        beta_dropdown: gr.update(visible=show_beta, value="Automatic" if show_beta else None),
    }

with gr.Blocks(title="Geochemical Geothermometer") as demo:
    gr.Markdown(
        """
        # Geochemical Geothermometer
        Calculate subsurface temperature based on fluid chemistry.
        Enter ion concentrations in mg/L and select method.
        """
    )
    with gr.Row():
        with gr.Column():
            method_dropdown = gr.Dropdown(
                choices=[
                    "Na-K (Fournier, 1979)",
                    "Na-K (Giggenbach, 1988)",
                    "Na-K-Ca (Fournier & Truesdell, 1973)",
                    "Quartz (no steam loss)",
                    "Quartz (adiabatic cooling)"
                ],
                label="Geothermometer Method",
                value="Na-K (Fournier, 1979)"
            )
            na_input = gr.Number(label="Na (mg/L)", value=None, visible=True)
            k_input = gr.Number(label="K (mg/L)", value=None, visible=True)
            ca_input = gr.Number(label="Ca (mg/L)", value=None, visible=False)
            sio2_input = gr.Number(label="SiO2 (mg/L)", value=None, visible=False)
            beta_dropdown = gr.Dropdown(
                choices=["1/3", "4/3", "Automatic"],
                label="Ca correction factor (β)",
                value="Automatic",
                visible=False
            )
            calc_btn = gr.Button("Calculate")
        with gr.Column():
            output = gr.Textbox(label="Result", lines=6)
            gr.Markdown(
                """
                **Assumptions:**
                - Quartz geothermometers assume equilibrium with quartz.
                - Na-K methods assume deep reservoir equilibrium and no mixing.
                - Na-K-Ca method includes calcium correction; default iterative algorithm adjusts β based on temperature.
                """
            )

    method_dropdown.change(fn=update_inputs, inputs=method_dropdown, outputs=[na_input, k_input, ca_input, sio2_input, beta_dropdown])
    calc_btn.click(fn=compute, inputs=[method_dropdown, na_input, k_input, ca_input, sio2_input, beta_dropdown], outputs=output)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
