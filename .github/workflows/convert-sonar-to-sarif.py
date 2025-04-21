import json
import sys

# Cargar JSON desde el archivo de SonarCloud
with open('reports/sonar-report.json', 'r') as f:
    sonar_data = json.load(f)

# Estructura básica SARIF
sarif = {
    "version": "2.1.0",
    "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0.json",
    "runs": [{
        "tool": {
            "driver": {
                "name": "SonarCloud (custom to SARIF)",
                "informationUri": "https://sonarcloud.io/",
                "rules": []
            }
        },
        "results": []
    }]
}

# Añadir findings al SARIF
for issue in sonar_data.get("issues", []):
    result = {
        "ruleId": issue.get("rule", "unknown"),
        "level": "error" if issue.get("severity") in ["BLOCKER", "CRITICAL"] else "warning",
        "message": {
            "text": issue.get("message", "No description")
        },
        "locations": [{
            "physicalLocation": {
                "artifactLocation": {
                    "uri": issue.get("component", "unknown").split(":")[-1]
                },
                "region": {
                    "startLine": issue.get("line", 1)
                }
            }
        }]
    }

    sarif["runs"][0]["results"].append(result)

# Guardar archivo SARIF
with open('reports/sonar-report.sarif', 'w') as f:
    json.dump(sarif, f, indent=2)

print("✅ Convertido a SARIF correctamente.")
