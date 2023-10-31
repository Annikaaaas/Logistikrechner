from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_logistics_cost(quantity_intimcreme, quantity_lotion, quantity_reisegroesse, calculation_type="B2C"):
    # Kosten pro Einheit (Nettopreise)
    cost_per_unit = {
        "INBOUND - Einlagerung Palette": 0.01,
        "STORAGE - Lagerung Palette": 0.01,
        "OUTBOUND - Outbound": 1.52,
        "OUTBOUND - Pick & Pack": 0.60,
        "OUTBOUND - Pick & Pack 2": 0.30,  # Kosten, wenn zwei Produkte vom gleichen Typ bestellt werden
        "VERSAND - Sendung polstern": 0.34,
        "VERSAND - Seidenpapier & Sticker": 0.17,
        "VERSAND - Grußkarte": 0.17,
        "VERSAND - Polstermaterial": 0.03,
        "VERSAND - Seidenpapier & Etikett": 0.05,
        "VERSAND - Kartonage": 0.12,
        "VERSAND - Versand Warenpost": 2.71,
        "VERSAND - Versand Paket bis 31,5 kg": 6.14,
        "VERSAND - Karte": 0.04,
        "VERSAND - Versand Amazon": 3.70
    }
    
    # Gewicht der Produkte (in Gramm)
    weight_intimcreme = 95
    weight_lotion = 252.4
    weight_reisegroesse = 33
    
    # Preise der Produkte (Bruttopreise)
    price_intimcreme_brutto = 39.95
    price_lotion_brutto = 29.95
    price_reisegroesse_brutto = 19.95
    
    # Berechnung der Nettopreise
    price_intimcreme_netto = price_intimcreme_brutto / 1.19  # 19% Mehrwertsteuer
    price_lotion_netto = price_lotion_brutto / 1.19
    price_reisegroesse_netto = price_reisegroesse_brutto / 1.19
    
    # Berechnung der Gesamtkosten ohne Versand (Nettopreise)
    total_cost_without_shipping = 0
    
    # Kosten für Intimcreme
    total_cost_without_shipping += cost_per_unit["OUTBOUND - Outbound"] * quantity_intimcreme
    total_cost_without_shipping += cost_per_unit["STORAGE - Lagerung Palette"] * quantity_intimcreme
    total_cost_without_shipping += cost_per_unit["INBOUND - Einlagerung Palette"] * quantity_intimcreme

    # Wenn mehr als ein Produkt Intimcreme bestellt wurde und die Anzahl gerade ist, verwende Pick & Pack 2
    if quantity_intimcreme > 1 and quantity_intimcreme % 2 == 0:
        total_cost_without_shipping += cost_per_unit["OUTBOUND - Pick & Pack 2"] * quantity_intimcreme
    else:
        total_cost_without_shipping += cost_per_unit["OUTBOUND - Pick & Pack"] * quantity_intimcreme
    
    # Kosten für Intimcreme Reisegröße
    total_cost_without_shipping += cost_per_unit["OUTBOUND - Outbound"] * quantity_reisegroesse
    total_cost_without_shipping += cost_per_unit["STORAGE - Lagerung Palette"] * quantity_reisegroesse
    total_cost_without_shipping += cost_per_unit["INBOUND - Einlagerung Palette"] * quantity_reisegroesse
    
    # Wenn mehr als ein Produkt Intimcreme Reisegröße bestellt wurde und die Anzahl gerade ist, verwende Pick & Pack 2
    if quantity_reisegroesse > 1 and quantity_reisegroesse % 2 == 0:
        total_cost_without_shipping += cost_per_unit["OUTBOUND - Pick & Pack 2"] * quantity_reisegroesse
    else:
        total_cost_without_shipping += cost_per_unit["OUTBOUND - Pick & Pack"] * quantity_reisegroesse
    
    # Kosten für Intimwaschlotion
    total_cost_without_shipping += cost_per_unit["OUTBOUND - Outbound"] * quantity_lotion
    total_cost_without_shipping += cost_per_unit["STORAGE - Lagerung Palette"] * quantity_lotion
    total_cost_without_shipping += cost_per_unit["INBOUND - Einlagerung Palette"] * quantity_lotion
    
    # Wenn mehr als ein Produkt Intimwaschlotion bestellt wurde und die Anzahl gerade ist, verwende Pick & Pack 2
    if quantity_lotion > 1 and quantity_lotion % 2 == 0:
        total_cost_without_shipping += cost_per_unit["OUTBOUND - Pick & Pack 2"] * quantity_lotion
    else:
        total_cost_without_shipping += cost_per_unit["OUTBOUND - Pick & Pack"] * quantity_lotion
    
    # Prüfung des Versands basierend auf dem Gesamtgewicht
    total_weight = (quantity_intimcreme * weight_intimcreme + quantity_lotion * weight_lotion + quantity_reisegroesse * weight_reisegroesse) / 1000
    
    shipping_cost = 0
    if total_weight <= 190:
        shipping_cost = cost_per_unit["VERSAND - Versand Warenpost"]
    else:
        shipping_cost = cost_per_unit["VERSAND - Versand Paket bis 31,5 kg"]
    

    # Einmalige Materialkosten
    cost_material = cost_per_unit[ "VERSAND - Sendung polstern"] + cost_per_unit[ "VERSAND - Seidenpapier & Sticker"] + cost_per_unit["VERSAND - Grußkarte"] + cost_per_unit["VERSAND - Polstermaterial"] + cost_per_unit["VERSAND - Seidenpapier & Etikett"] + cost_per_unit["VERSAND - Kartonage"] + cost_per_unit["VERSAND - Karte"]


    # Hinzufügen der Versandkosten zu den Gesamtkosten
    total_cost_with_shipping_and_materials = total_cost_without_shipping + shipping_cost + cost_material
    
    # Berechnung des Gesamtnetto-Preiswerts der Produkte
    total_netto_value = (price_intimcreme_netto * quantity_intimcreme + price_lotion_netto * quantity_lotion + price_reisegroesse_netto * quantity_reisegroesse)
    
    
    # Überprüfung, ob der Nettowarenkorb-Wert unter oder über 50 Euro liegt
    if total_netto_value < 50:
        total_netto_value += 3.95  # Füge 3,95 Euro hinzu, wenn der Wert unter 50 Euro liegt
        shipping_message = "Der Kunde zahlt die Versandkosten in Höhe von 3,95 Euro."
    else:
        shipping_message = "Kostenloser Versand für den Kunden."

    # Berechnung der prozentualen Kosten mit und ohne Versand
    percentage_cost_with_shipping = (total_cost_with_shipping_and_materials / total_netto_value) * 100
    percentage_cost_without_shipping = (total_cost_without_shipping / total_netto_value) * 100
    
    return round(total_cost_with_shipping_and_materials, 2), round(total_cost_without_shipping, 2), round(total_netto_value, 2), round(percentage_cost_with_shipping, 2), round(percentage_cost_without_shipping, 2), shipping_message


def calculate_b2b_logistics_cost(quantity_intimcreme, quantity_lotion, quantity_reisegroesse):
    # B2B-spezifische Logik hier
    # Kosten pro Einheit (Nettopreise)
    cost_per_unit = {
        "INBOUND - Einlagerung Palette": 0.01,
        "STORAGE - Lagerung Palette": 0.01,
        "OUTBOUND - Outbound": 1.52,
        "OUTBOUND - Pick & Pack": 0.60,
        "VERSAND - Versandtasche": 0.09,
        "VERSAND - Versand Paket bis 31,5 kg": 6.14
    }

    # Gewicht der Produkte (in Gramm)
    weight_intimcreme = 95
    weight_lotion = 252.4
    weight_reisegroesse = 33

    # Berechnung der Anzahl der benötigten Verpackungseinheiten (VPE) für Intimcreme, Lotion und Reisegröße
    num_vpes_intimcreme = quantity_intimcreme // 24
    num_vpes_lotion = quantity_lotion // 30
    num_vpes_reisegroesse = quantity_reisegroesse // 54

    # Berechnung der Kosten ohne Versand basierend auf VPEs
    total_cost_without_shipping = cost_per_unit["STORAGE - Lagerung Palette"] + cost_per_unit["INBOUND - Einlagerung Palette"]
    total_cost_without_shipping += cost_per_unit["OUTBOUND - Pick & Pack"] * (num_vpes_intimcreme + num_vpes_lotion + num_vpes_reisegroesse)+ cost_per_unit["OUTBOUND - Outbound"]

    # Berechnung der verbleibenden Produkte nach Abzug der VPEs
    remaining_intimcreme = quantity_intimcreme % 24
    remaining_lotion = quantity_lotion % 30
    remaining_reisegroesse = quantity_reisegroesse % 54

    total_cost_without_shipping += cost_per_unit["OUTBOUND - Pick & Pack"] * (remaining_intimcreme + remaining_lotion + remaining_reisegroesse)

    # Berechnung der Anzahl der benötigten Pakete für den Versand basierend auf den restlichen Produkten
    num_packages = (num_vpes_intimcreme + num_vpes_lotion + num_vpes_reisegroesse)

    if remaining_intimcreme > 0 or remaining_lotion > 0 or remaining_reisegroesse > 0:
        num_packages += 1
    # Berechnung der Kosten für den Versand (Outbound) der restlichen Produkte einzeln
    total_cost_without_shipping += cost_per_unit["VERSAND - Versandtasche"] * (remaining_intimcreme + remaining_lotion + remaining_reisegroesse+ num_vpes_intimcreme + num_vpes_lotion + num_vpes_reisegroesse )

    # Berechnung der Versandkosten basierend auf der Anzahl der benötigten Pakete
    shipping_cost = cost_per_unit["VERSAND - Versand Paket bis 31,5 kg"] * num_packages

    # Gesamtkosten mit Versand und Versandtaschen (Nettopreise)
    total_cost_with_shipping = total_cost_without_shipping + shipping_cost

    # Berechnung des Gesamtnettowarenwertes
    price_intimcreme_brutto = 12.5
    price_lotion_brutto = 9.37
    price_reisegroesse_brutto = 1.9

    price_intimcreme_netto = price_intimcreme_brutto / 1.19
    price_lotion_netto = price_lotion_brutto / 1.19
    price_reisegroesse_netto = price_reisegroesse_brutto / 1.19

    total_netto_value = (quantity_intimcreme * price_intimcreme_netto) + (quantity_lotion * price_lotion_netto) + (quantity_reisegroesse * price_reisegroesse_netto)

    # Berechnung des prozentualen Anteils der Gesamtkosten an dem Gesamtnettowarenwert (mit und ohne Versand)
    percentage_cost_with_shipping = (total_cost_with_shipping / total_netto_value) * 100
    percentage_cost_without_shipping = (total_cost_without_shipping / total_netto_value) * 100

    # Initialisiere shipping_message als leeren String
    shipping_message = ""
    
    return round(total_cost_with_shipping, 2), round(total_cost_without_shipping, 2), round(total_netto_value, 2), round(percentage_cost_with_shipping, 2), round(percentage_cost_without_shipping, 2), shipping_message


def calculate_amazon_logistics_cost(quantity_intimcreme, quantity_lotion, quantity_reisegroesse):
    cost_per_unit = {
        "INBOUND - Einlagerung Palette": 0.01,
        "STORAGE - Lagerung Palette": 0.01,
        "OUTBOUND - Outbound": 1.52,
        "OUTBOUND - Pick & Pack": 0.60,
        "VERSAND - Versandtasche": 0.09,
        "VERSAND - Versand Paket": 3.70  # Korrigierte Bezeichnung
    }

    # Gewicht der Produkte (in Gramm)
    weight_intimcreme = 95
    weight_lotion = 252.4
    weight_reisegroesse = 33

    # Berechnung der Anzahl der benötigten Verpackungseinheiten (VPE) für Intimcreme, Lotion und Reisegröße
    num_vpes_intimcreme = quantity_intimcreme // 24
    num_vpes_lotion = quantity_lotion // 30
    num_vpes_reisegroesse = quantity_reisegroesse // 54

    # Berechnung der Kosten ohne Versand basierend auf VPEs
    total_cost_without_shipping = cost_per_unit["STORAGE - Lagerung Palette"] + cost_per_unit["INBOUND - Einlagerung Palette"]
    total_cost_without_shipping += cost_per_unit["OUTBOUND - Pick & Pack"] * (num_vpes_intimcreme + num_vpes_lotion + num_vpes_reisegroesse)+ cost_per_unit["OUTBOUND - Outbound"]

    # Berechnung der verbleibenden Produkte nach Abzug der VPEs
    remaining_intimcreme = quantity_intimcreme % 24
    remaining_lotion = quantity_lotion % 30
    remaining_reisegroesse = quantity_reisegroesse % 54

    total_cost_without_shipping += cost_per_unit["OUTBOUND - Pick & Pack"] * (remaining_intimcreme + remaining_lotion + remaining_reisegroesse)

    # Berechnung der Anzahl der benötigten Pakete für den Versand basierend auf den restlichen Produkten
    num_packages = (num_vpes_intimcreme + num_vpes_lotion + num_vpes_reisegroesse)

    if remaining_intimcreme > 0 or remaining_lotion > 0 or remaining_reisegroesse > 0:
        num_packages += 1
    # Berechnung der Kosten für den Versand (Outbound) der restlichen Produkte einzeln
    total_cost_without_shipping += cost_per_unit["VERSAND - Versandtasche"] * (remaining_intimcreme + remaining_lotion + remaining_reisegroesse+ num_vpes_intimcreme + num_vpes_lotion + num_vpes_reisegroesse )

    # Berechnung der Versandkosten basierend auf der Anzahl der benötigten Pakete
    shipping_cost = cost_per_unit["VERSAND - Versand Paket"] * num_packages

    # Gesamtkosten mit Versand und Versandtaschen (Nettopreise)
    total_cost_with_shipping = total_cost_without_shipping + shipping_cost

    # Preise der Produkte (Bruttopreise)
    price_intimcreme_brutto = 39.95
    price_lotion_brutto = 29.95
    price_reisegroesse_brutto = 19.95

    price_intimcreme_netto = price_intimcreme_brutto / 1.19
    price_lotion_netto = price_lotion_brutto / 1.19
    price_reisegroesse_netto = price_reisegroesse_brutto / 1.19

    total_netto_value = (quantity_intimcreme * price_intimcreme_netto) + (quantity_lotion * price_lotion_netto) + (quantity_reisegroesse * price_reisegroesse_netto)

    # Berechnung des prozentualen Anteils der Gesamtkosten an dem Gesamtnettowarenwert (mit und ohne Versand)
    percentage_cost_with_shipping = (total_cost_with_shipping / total_netto_value) * 100
    percentage_cost_without_shipping = (total_cost_without_shipping / total_netto_value) * 100

    # Initialisiere shipping_message als leeren String
    shipping_message = ""
    
    return round(total_cost_with_shipping, 2), round(total_cost_without_shipping, 2), round(total_netto_value, 2), round(percentage_cost_with_shipping, 2), round(percentage_cost_without_shipping, 2), shipping_message

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        calculation_type = request.form["calculation_type"]
        quantity_intimcreme = int(request.form["quantity_intimcreme"])
        quantity_lotion = int(request.form["quantity_lotion"])
        quantity_reisegroesse = int(request.form["quantity_reisegroesse"])
        
        if calculation_type == "B2B":
            total_cost_with_shipping_and_materials, total_cost_without_shipping, total_netto_value, percentage_cost_with_shipping, percentage_cost_without_shipping, shipping_message = calculate_b2b_logistics_cost(quantity_intimcreme, quantity_lotion, quantity_reisegroesse)
        elif calculation_type == "Amazon":
            total_cost_with_shipping_and_materials, total_cost_without_shipping, total_netto_value, percentage_cost_with_shipping, percentage_cost_without_shipping, shipping_message = calculate_amazon_logistics_cost(quantity_intimcreme, quantity_lotion, quantity_reisegroesse)
        else:
            total_cost_with_shipping_and_materials, total_cost_without_shipping, total_netto_value, percentage_cost_with_shipping, percentage_cost_without_shipping, shipping_message= calculate_logistics_cost(quantity_intimcreme, quantity_lotion, quantity_reisegroesse)
        
        return render_template("result.html", total_cost_with_shipping_and_materials=total_cost_with_shipping_and_materials, total_cost_without_shipping=total_cost_without_shipping, total_netto_value=total_netto_value, percentage_cost_with_shipping=percentage_cost_with_shipping, percentage_cost_without_shipping=percentage_cost_without_shipping, shipping_message=shipping_message)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
