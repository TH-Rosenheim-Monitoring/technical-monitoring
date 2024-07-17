# technical-monitoring-helper-methods - documentation in English

## Table of Contents

- [plausibility_filter](#plausibility_filter)
- [loc_colreg](#loc_colreg)
- [plot_conditional_marking](#plot_conditional_marking)
- [df_time_intersection](#df_time_intersection)
- [detect_real_timeresolution](#detect_real_timeresolution)
- [detect_real_timeresolution_df](#detect_real_timeresolution_df)
- [identify_supply_return](#identify_supply_return)
- [df_clusterTime_function](#df_clusterTime_function)
- [pullzero](#pullzero)
- [resample2equidistance](#resample2equidistance)
- [desum_formBased](#desum_formBased)
- [desum_period_based](#desum_period_based)


## plausibility_filter

### Description
The `plausibility_filter` function removes timestamps with values or derivatives of them outside a defined range or marks them as invalid. The range is based on empirical values.

### Arguments
- `h`: `pandas DataFrame`
  - The DataFrame where values should be checked and filtered if necessary.
- `ran`: `list`
  - List of conditions that must be fulfilled:
    1. `ran[0]`: Lower limit.
    2. `ran[1]`: Upper limit.
    3. `ran[2]` (Optional): List of regular expressions where at least one must match to include columns in the check.
    4. `ran[3]` (Optional): Degree of derivative of the values to be checked and filtered instead of the actual values.
- `b_verbose`: `bool` (default: `False`)
  - If `True`, prints the exceed rate.

### Returns
- `h_`: `pandas DataFrame`
  - The initial DataFrame with values filtered where conditions are fulfilled.

---

## loc_colreg

### Description
The `loc_colreg` function filters column names of a pandas DataFrame using regular expressions.

### Arguments
- `df`: `pandas DataFrame`
  - The DataFrame where column names should be filtered.
- `regexs`: `str` or `list`
  - One or more regular expressions to search in the columns of the provided DataFrame.
- `bs_inverse`: `bool` (default: `False`)
  - Activate negation of search results.
- `b_or_operation`: `bool` (default: `False`)
  - Activate OR operation with search matches.

### Returns
- `df`: `pandas DataFrame`
  - DataFrame with columns filtered based on the regular expressions provided.

---

## plot_conditional_marking

### Description
The `plot_conditional_marking` function plots a marker area in time periods where a given condition is fulfilled over an existing plot.

### Arguments
- `cond`: `pandas DataFrame`
  - Boolean DataFrame indicating where the condition is fulfilled.
- `color`: `str` (default: `"yellow"`)
  - Color of the marking area.
- `alpha`: `float` (default: `0.5`)
  - Opacity of the marking area.
- `ax`: `matplotlib axis` object (optional)
  - Existing axis object where marking area should be plotted.
- `limits`: `list` (optional)
  - List of lower and upper limit of marking area.
- `label`: `str` (default: `"_hidden"`)
  - Label of marking area for legend.
- `b_use_fill_between`: `bool` (default: `True`)
  - Use `fill_between` function from matplotlib.

### Returns
- `ax`: `matplotlib axis` object
  - Modified axis object with the marking area plotted.

---

## df_time_intersection

### Description
The `df_time_intersection` function calculates the temporal intersection of two pandas DataFrames and returns them with reduced but common time range.

### Arguments
- `df1`: `pandas DataFrame`
  - First DataFrame.
- `df2`: `pandas DataFrame`
  - Second DataFrame.

### Returns
- `df1`: `pandas DataFrame`
  - First DataFrame with common time range.
- `df2`: `pandas DataFrame`
  - Second DataFrame with common time range.

---

## detect_real_timeresolution

### Description
The `detect_real_timeresolution` function detects the real time resolution in a time series where values are actualized.

### Arguments
- `s`: `pandas time series`
  - Time series data.

### Returns
- `s`: `pandas time series`
  - Time series of time resolutions.

---

## detect_real_timeresolution_df

### Description
The `detect_real_timeresolution_df` function detects the real time resolution in a DataFrame where values are actualized.

### Arguments
- `df`: `pandas DataFrame`
  - DataFrame with time series data.

### Returns
- `df`: `pandas DataFrame`
  - DataFrame of time resolutions.

---

## identify_supply_return

### Description
The `identify_supply_return` function checks whether more energy flows into supply or return based on heat meter time series.

### Arguments
- `df`: `pandas DataFrame`
  - DataFrame of heat meter time series.
- `c`: `float` (default: `4.18`)
  - Specific heat capacity of the medium (defaults to water).

### Returns
- `energy_netto`: `float`
  - Netto energy return and supply.

---

## df_clusterTime_function

### Description
The `df_clusterTime_function` function determines time intervals where a specific condition occurs and calculates a desired quantity for each interval.

### Arguments
- `d`: `pandas time series`
  - Time series data.

### Returns
- `d`: `pandas time series`
  - Time series data.

---

## pullzero

### Description
The `pullzero` function subtracts the initial value of each counter time series so that all time series start at 0.

### Arguments
- `df`: `pandas DataFrame`
  - DataFrame of counter time series that should start at zero.

### Returns
- `df`: `pandas DataFrame`
  - DataFrame of counter time series starting at zero.

---

## resample2equidistance

### Description
The `resample2equidistance` function completes time series for each time step based on a defined temporal resolution.

### Arguments
- `df`: `pandas DataFrame`
  - DataFrame with time series that should be equidistant.
- `freq`: `str` (default: `"min"`)
  - Time unit for equidistantiation.

### Returns
- `df`: `pandas DataFrame`
  - DataFrame with equidistant time series.

---

## desum_formBased

### Description
The `desum_formBased` function divides a data series into two summands based on given criteria.

### Arguments
- `ts`: `pandas time series`
  - Time series data.
- `threshold`: `int` (default: `5`)
  - Threshold that must be exceeded for the second part to be considered active.
- `ws`: `int` (default: `30`)
  - Window size for the moving average calculation of the first part.
- `min_periods`: `int` (default: `5`)
  - Minimum time units that threshold must be exceeded for the second part to be considered active.
- `b_visualize`: `bool` (default: `False`)
  - If `True`, results will be plotted.

### Returns
- `pd.concat([summand1, summand2], axis=1)`: `pandas DataFrame`
  - Two pandas time series representing the splitted time series.

---

## desum_period_based

### Description
The `desum_period_based` function disaggregates the values of a time series into multiple time series based on different periodicities.

### Arguments
- `p`: `pandas time series`
  - Time series that should be disaggregated.
- `characterizing_periods`: `list` (default: `[60, 1440]`)
  - List of period durations in minutes that characterize the suspected consumers.
- `b_visualize`: `bool` (default: `True`)
  - If `True`, plot a visualization of the disaggregated time series.

### Returns
- `pp`: `pandas DataFrame`
  - Multiple pandas time series representing the splitted time series.

  
# technical-monitoring-helper-methods - Dokumentation auf Deutsch

## Inhaltsverzeichnis

- [plausibility_filter](#plausibility_filter)
- [loc_colreg](#loc_colreg)
- [plot_conditional_marking](#plot_conditional_marking)
- [df_time_intersection](#df_time_intersection)
- [detect_real_timeresolution](#detect_real_timeresolution)
- [detect_real_timeresolution_df](#detect_real_timeresolution_df)
- [identify_supply_return](#identify_supply_return)
- [df_clusterTime_function](#df_clusterTime_function)
- [pullzero](#pullzero)
- [resample2equidistance](#resample2equidistance)
- [desum_formBased](#desum_formBased)
- [desum_period_based](#desum_period_based)
  
## plausibility_filter

### Beschreibung
Die Funktion `plausibility_filter` entfernt Zeitstempel mit Werten oder Ableitungen außerhalb eines definierten Bereichs oder markiert sie als ungültig. Der Bereich basiert auf empirischen Werten.

### Argumente
- `h`: `pandas DataFrame`
  - Der DataFrame, in dem Werte überprüft und bei Bedarf gefiltert werden sollen.
- `ran`: `Liste`
  - Liste von Bedingungen, die erfüllt sein müssen:
    1. `ran[0]`: Untere Grenze.
    2. `ran[1]`: Obere Grenze.
    3. `ran[2]` (Optional): Liste von regulären Ausdrücken, von denen mindestens einer mit Spaltennamen übereinstimmen muss.
    4. `ran[3]` (Optional): Ableitungsgrad der Werte, der überprüft und gefiltert werden soll, anstelle der tatsächlichen Werte.
- `b_verbose`: `bool` (Standard: `False`)
  - Wenn `True`, wird die Überschreitungsrate ausgegeben.

### Rückgabe
- `h_`: `pandas DataFrame`
  - Der ursprüngliche DataFrame mit gefilterten Werten, wo die Bedingungen erfüllt sind.

---

## loc_colreg

### Beschreibung
Die Funktion `loc_colreg` filtert Spaltennamen eines pandas DataFrames mithilfe regulärer Ausdrücke.

### Argumente
- `df`: `pandas DataFrame`
  - Der DataFrame, dessen Spaltennamen gefiltert werden sollen.
- `regexs`: `str` oder `Liste`
  - Ein oder mehrere reguläre Ausdrücke, die in den Spaltennamen des bereitgestellten DataFrames gesucht werden sollen.
- `bs_inverse`: `bool` (Standard: `False`)
  - Aktiviert die Negation der Suchergebnisse.
- `b_or_operation`: `bool` (Standard: `False`)
  - Aktiviert die ODER-Verknüpfung mit den Suchergebnissen.

### Rückgabe
- `df`: `pandas DataFrame`
  - DataFrame mit Spalten, die auf Grundlage der bereitgestellten regulären Ausdrücke gefiltert wurden.

---

## plot_conditional_marking

### Beschreibung
Die Funktion `plot_conditional_marking` zeichnet einen Markierungsbereich in Zeitabschnitten, in denen eine bestimmte Bedingung erfüllt ist, über einem vorhandenen Plot.

### Argumente
- `cond`: `pandas DataFrame`
  - Boolescher DataFrame, der anzeigt, wo die Bedingung erfüllt ist.
- `color`: `str` (Standard: `"yellow"`)
  - Farbe des Markierungsbereichs.
- `alpha`: `float` (Standard: `0.5`)
  - Opazität des Markierungsbereichs.
- `ax`: `matplotlib Achsenobjekt` (optional)
  - Vorhandenes Achsenobjekt, in dem der Markierungsbereich gezeichnet werden soll.
- `limits`: `Liste` (optional)
  - Liste mit unterer und oberer Grenze des Markierungsbereichs.
- `label`: `str` (Standard: `"_hidden"`)
  - Beschriftung des Markierungsbereichs für die Legende.
- `b_use_fill_between`: `bool` (Standard: `True`)
  - Verwendung der `fill_between` Funktion von matplotlib.

### Rückgabe
- `ax`: `matplotlib Achsenobjekt`
  - Modifiziertes Achsenobjekt mit dem gezeichneten Markierungsbereich.

---

## df_time_intersection

### Beschreibung
Die Funktion `df_time_intersection` berechnet die zeitliche Schnittmenge von zwei pandas DataFrames und gibt sie mit reduziertem, aber gemeinsamem Zeitbereich zurück.

### Argumente
- `df1`: `pandas DataFrame`
  - Erster DataFrame.
- `df2`: `pandas DataFrame`
  - Zweiter DataFrame.

### Rückgabe
- `df1`: `pandas DataFrame`
  - Erster DataFrame mit gemeinsamem Zeitbereich.
- `df2`: `pandas DataFrame`
  - Zweiter DataFrame mit gemeinsamem Zeitbereich.

---

## detect_real_timeresolution

### Beschreibung
Die Funktion `detect_real_timeresolution` erkennt die tatsächliche Zeitauflösung in einer Zeitreihe, in der Werte aktualisiert werden.

### Argumente
- `s`: `pandas Zeitreihe`
  - Zeitreihendaten.

### Rückgabe
- `s`: `pandas Zeitreihe`
  - Zeitreihe der Zeitauflösungen.

---

## detect_real_timeresolution_df

### Beschreibung
Die Funktion `detect_real_timeresolution_df` erkennt die tatsächliche Zeitauflösung in einem DataFrame, in dem Werte aktualisiert werden.

### Argumente
- `df`: `pandas DataFrame`
  - DataFrame mit Zeitreihendaten.

### Rückgabe
- `df`: `pandas DataFrame`
  - DataFrame der Zeitauflösungen.

---

## identify_supply_return

### Beschreibung
Die Funktion `identify_supply_return` überprüft, ob mehr Energie in die Versorgung oder Rückführung fließt, basierend auf Wärmemessdaten.

### Argumente
- `df`: `pandas DataFrame`
  - DataFrame von Wärmemessdaten.
- `c`: `float` (Standard: `4.18`)
  - Spezifische Wärmekapazität des Mediums (Standardmäßig Wasser).

### Rückgabe
- `energy_netto`: `float`
  - Netto-Energie Rück- und Zufuhr.

---

## df_clusterTime_function

### Beschreibung
Die Funktion `df_clusterTime_function` bestimmt Zeitintervalle, in denen eine spezifische Bedingung auftritt, und berechnet eine gewünschte Größe für jedes Intervall.

### Argumente
- `d`: `pandas Zeitreihe`
  - Zeitreihendaten.

### Rückgabe
- `d`: `pandas Zeitreihe`
  - Zeitreihendaten.

---

## pullzero

### Beschreibung
Die Funktion `pullzero` subtrahiert den Anfangswert jeder Zähler-Zeitreihe, sodass alle Zeitreihen bei 0 beginnen.

### Argumente
- `df`: `pandas DataFrame`
  - DataFrame von Zähler-Zeitreihen, die alle bei 0 beginnen sollen.

### Rückgabe
- `df`: `pandas DataFrame`
  - DataFrame von Zähler-Zeitreihen, die bei 0 beginnen.

---

## resample2equidistance

### Beschreibung
Die Funktion `resample2equidistance` vervollständigt Zeitreihen für jeden Zeitschritt basierend auf einer definierten zeitlichen Auflösung.

### Argumente
- `df`: `pandas DataFrame`
  - DataFrame mit Zeitreihen, die equidistant gemacht werden sollen.
- `freq`: `str` (Standard: `"min"`)
  - Zeitliche Einheit für die Equidistantisierung.

### Rückgabe
- `df`: `pandas DataFrame`
  - DataFrame mit equidistanten Zeitreihen.

---

## desum_formBased

### Beschreibung
Die Funktion `desum_formBased` teilt eine Datenreihe basierend auf bestimmten Kriterien in zwei Summanden auf.

### Argumente
- `ts`: `pandas Zeitreihe`
  - Zeitreihendaten.
- `threshold`: `int` (Standard: `5`)
  - Schwellenwert, der überschritten werden muss, damit der zweite Teil als aktiv betrachtet wird.
- `ws`: `int` (Standard: `30`)
  - Fenstergröße für die gleitende Durchschnittsberechnung des ersten Teils.
- `min_periods`: `int` (Standard: `5`)
  - Mindestanzahl von Zeiteinheiten, die überschritten werden müssen, damit der zweite Teil als aktiv betrachtet wird.
- `b_visualize`: `bool` (Standard: `False`)
  - Wenn `True`, werden die Ergebnisse geplottet.

### Rückgabe
- `pd.concat([summand1, summand2], axis=1)`: `pandas DataFrame`
  - Zwei pandas Zeitreihen, die die aufgeteilte Zeitreihe darstellen.

---

## desum_period_based

### Beschreibung
Die Funktion `desum_period_based` disaggregiert die Werte einer Zeitreihe in mehrere Zeitreihen basierend auf verschiedenen Periodizitäten.

### Argumente
- `p`: `pandas Zeitreihe`
  - Zeitreihe, die disaggregiert werden soll.
- `characterizing_periods`: `Liste` (Standard: `[60, 1440]`)
  - Liste von Periodendauern in Minuten, die die vermuteten Verbra

