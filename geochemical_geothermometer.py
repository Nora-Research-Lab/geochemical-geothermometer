import math

def calculate_temperature(method, conc, beta=None):
    """
    Calculate temperature using specified geothermometer method.
    conc: dict with keys 'Na', 'K', 'Ca', 'SiO2' as needed.
    beta: for Na-K-Ca method, if None use iterative approach.
    Returns temperature in Celsius.
    """
    if method == "Na-K (Fournier, 1979)":
        na = conc['Na']
        k = conc['K']
        if na <= 0 or k <= 0:
            raise ValueError("Na and K must be positive.")
        ratio = na / k
        if ratio <= 0:
            raise ValueError("Na/K ratio must be positive.")
        try:
            T = 1217.0 / (math.log10(ratio) + 1.483) - 273.15
        except (OverflowError, ValueError) as e:
            raise ValueError("Calculation error: possibly invalid ratio.") from e
        return T

    elif method == "Na-K (Giggenbach, 1988)":
        na = conc['Na']
        k = conc['K']
        if na <= 0 or k <= 0:
            raise ValueError("Na and K must be positive.")
        ratio = na / k
        if ratio <= 0:
            raise ValueError("Na/K ratio must be positive.")
        try:
            T = 1390.0 / (math.log10(ratio) + 1.750) - 273.15
        except (OverflowError, ValueError) as e:
            raise ValueError("Calculation error.") from e
        return T

    elif method == "Na-K-Ca (Fournier & Truesdell, 1973)":
        na = conc['Na']
        k = conc['K']
        ca = conc['Ca']
        if na <= 0 or k <= 0 or ca <= 0:
            raise ValueError("Na, K, and Ca must be positive.")
        if beta is None:
            # Iterative: start with beta = 1/3
            beta = 1.0/3.0
            T = 1647.0 / (math.log10(na/k) + beta * math.log10(math.sqrt(ca)/na) + 2.24) - 273.15
            if T >= 100.0:
                beta = 4.0/3.0
                T = 1647.0 / (math.log10(na/k) + beta * math.log10(math.sqrt(ca)/na) + 2.24) - 273.15
        else:
            # Use provided beta
            T = 1647.0 / (math.log10(na/k) + beta * math.log10(math.sqrt(ca)/na) + 2.24) - 273.15
        return T

    elif method == "Quartz (no steam loss)":
        sio2 = conc['SiO2']
        if sio2 <= 0:
            raise ValueError("SiO2 must be positive.")
        try:
            log_sio2 = math.log10(sio2)
        except ValueError:
            raise ValueError("SiO2 must be positive.")
        T = 72.5 * (log_sio2 ** 2) - 36.0 * log_sio2 + 42.4
        return T

    elif method == "Quartz (adiabatic cooling)":
        sio2 = conc['SiO2']
        if sio2 <= 0:
            raise ValueError("SiO2 must be positive.")
        try:
            log_sio2 = math.log10(sio2)
        except ValueError:
            raise ValueError("SiO2 must be positive.")
        T = 42.2 * (log_sio2 ** 2) - 22.0 * log_sio2 + 24.4
        return T

    else:
        raise ValueError(f"Unknown method: {method}")

def enthalpy_class(temperature_celsius):
    if temperature_celsius < 100.0:
        return "Low enthalpy (<100°C)"
    elif 100.0 <= temperature_celsius <= 200.0:
        return "Medium enthalpy (100-200°C)"
    else:
        return "High enthalpy (>200°C)"
