import os, sys, json, argparse

def read_field(field_name, obj):
  try:
    field_value = obj[field_name]
  except Exception as e:
    return ""
  return field_value

def get_filename(classMessage):
  try:
    file_name = classMessage.split("(", 1)[0].strip()
  except Exception as e:
    return ""
  return file_name

def total_findings(json_file):
  issues = {'critical': 0, 'high': 0, 'medium': 0, 'weak': 0}
  ignored = {'critical': 0, 'high': 0, 'medium': 0, 'weak': 0}

  weak = []
  medium = []
  high = []
  critical = []

  weak_cnt = 0
  medium_cnt = 0
  high_cnt = 0
  critical_cnt = 0
  total_cnt = 0

  weak_cwe = []
  medium_cwe = []
  high_cwe = []
  critical_cwe = []

  with open(json_file) as json_f:
    data = json.load(json_f)

    # # Get counts
    weak_cnt = 0
    medium_cnt = 0
    high_cnt = 0
    critical_cnt = 0
    total_cnt = 0

    for vulngrp in data["analysisVulnerabilities"]:
      vuln = vulngrp["vulnerabilities"]
      # Read each field
      vulnerabilityID = read_field("vulnerabilityID", vuln)
      line = read_field("line", vuln)
      col = read_field("column", vuln)
      confidence = read_field("confidence", vuln).lower()
      file_name = read_field("file", vuln)
      code = read_field("code", vuln)
      details = read_field("details", vuln)
      severity = read_field("severity", vuln).lower()
      rule_id = read_field("rule_id", vuln)
      vuln_hash = read_field("vulnHash", vuln)
      lang = read_field("language", vuln)
      warn_type = read_field("type", vuln)

      if severity == "unknown":
        severity = "weak"

      if confidence == "unknown":
        confidence = "weak"

      if severity == "low":
        severity = "weak"

      if confidence == "low":
        confidence = "weak"

      # Pack as a structure
      finding = {
        vuln_hash: {
          "vuln_id": vulnerabilityID,
          "warning_type": warn_type,
          "check_name": rule_id,
          "message": details,
          "file": file_name,
          "line": line,
          "col": col,
          "language": lang,
          "severity": severity,
          "confidence": confidence,
          "code": code
        }
      }

      # Append to each severity level
      if severity == "weak":
        weak.append(finding)
        weak_cnt += 1
        if not rule_id in weak_cwe:
          weak_cwe.append(rule_id)
      elif severity == "medium":
        medium.append(finding)
        medium_cnt += 1
        if not rule_id in medium_cwe:
          medium_cwe.append(rule_id)
      elif severity == "high":
        high.append(finding)
        high_cnt += 1
        if not rule_id in high_cwe:
          high_cwe.append(rule_id)
      else:
        critical.append(finding)
        critical_cnt += 1
        if not rule_id in critical_cwe:
          critical_cwe.append(rule_id)

  total_cnt = weak_cnt + medium_cnt + high_cnt + critical_cnt

  # Build the final result object
  out = {
    "warnings": {
      "critical": critical_cnt,
      "high": high_cnt,
      "medium": medium_cnt,
      "weak": weak_cnt,
      "total": total_cnt
    },
    "ignored_warnings": {
      "critical": 0,
      "high": 0,
      "medium": 0,
      "weak": 0
    },
    "findings": {
      "critical": critical_cwe,
      "high": high_cwe,
      "medium": medium_cwe,
      "weak": weak_cwe
    },
    "fingerprints": {
      "critical": critical,
      "high": high,
      "medium": medium,
      "weak": weak
    }
  }

  return json.dumps(out, indent=2)

def write_outfile(json_obj, out_file):
  f = open(out_file, "w")
  f.write(json_obj)
  f.close()

def main():
  parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument('-i', '--input', type=str, required=True, help='The insider input JSON file.')
  parser.add_argument('-o', '--output', type=str, required=False, default="stdout", help='Specify an output file. If left empty prints to stdout.')
  args = parser.parse_args()

  in_file = args.input
  out_file = args.output

  if not os.path.isfile(in_file):
    print("Please specify an existing input JSON file.")
    sys.exit(2)

  results = total_findings(in_file)

  if out_file == "stdout":
    print(results)
  else:
    write_outfile(results, out_file)

if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print("Exception occured.", str(e))
    sys.exit(1)
