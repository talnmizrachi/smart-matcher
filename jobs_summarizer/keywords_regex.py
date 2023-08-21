KEYWORDS_MAPPING = {
    "backend": "back.?end",
    "frontend": "front.?end",
    "fullstack": "full.?stack",
    "software": "software",
    "mobile": "mobile",
    "swift": "swift",
    "objectivec": "objective c",
    "android": "android",
    "ios": "ios",
    "rest": "rest\\s?api",
    "tcpip": "tcp/ip|tcp",
    "socket": "socket",
    "docker": "docker",
    "cloud": "cloud",
    "gcp": "google cloud|gcp",
    "azure": "azure",
    "python": "python",
    "java": "java",
    "golang": "golang",
    "nodejs": "node|node.js|nodejs",
    "csharp": "c#",
    "c": "c",
    "cpp": "c\\+\\+",
    "assembly": "assembly",
    "javascript": "javascript",
    "ruby": "ruby",
    "html": "html",
    "css": "css",
    "linux": "linux",
    "posix": "posix",
    "database": "database",
    "nosql": "nosql",
    "mongo": "mongo",
    "postgres": "postgres",
    "mssql": "mssql",
    "mysql": "mysql",
    "oracle": "oracle",
    "git": "git",
    "angular": "angular",
    "react": "react",
    "vue": "vue",
    "agile": "agile",
    "oop": "oop|object oriented",
    "embedded": "embedded",
    "message_broker": "message broker",
    "kafka": "kafka",
    "rabbitmq": "rabbit",
    "graphql": "graphql",
    "data_analytics": "(data analytics|data analysis|data analyst)",
    "data_science": "(data science|data scientist)",
    "data_engineer": "(data engineer|data engineering)",
    "big_data": "big data",
    "machine_learning": "machine learning",
    "artificial_intelligence": "artificial intelligence",
    "ai": "ai",
    "ml": "ml",
    "deep_learning": "deep learning",
    "nlp": "(natural language processing|nlp)",
    "computer_vision": "computer vision",
    "data_mining": "data mining",
    "statistics": "statistics",
    "predictive_modeling": "predictive modeling",
    "regression": "regression",
    "classification": "classification",
    "clustering": "clustering",
    "r": "r",
    "sas": "sas",
    "spss": "spss",
    "matlab": "matlab",
    "julia": "julia",
    "sql": "sql",
    "hadoop": "hadoop",
    "spark": "spark",
    "hive": "hive",
    "pig": "pig",
    "mapreduce": "mapreduce",
    "tensorflow": "tensorflow",
    "keras": "keras",
    "pytorch": "pytorch",
    "scikit_learn": "scikit[-]?learn",
    "pandas": "pandas",
    "numpy": "numpy",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "ggplot": "ggplot",
    "bi": "(business intelligence|bi)",
    "tableau": "tableau",
    "powerbi": "power[\\s]?bi",
    "qlik": "qlik",
    "d3_js": "d3.js",
    "excel": "excel",
    "data_visualization": "data visualization",
    "data_cleaning": "data cleaning",
    "data_wrangling": "data wrangling",
    "data_integration": "data integration",
    "etl": "etl",
    "elt": "elt",
    "data_pipeline": "data pipeline",
    "feature_engineering": "feature engineering",
    "ab_testing": "(a/b|ab) testing",
    "time_series": "time series",
    "anomaly_detection": "anomaly detection",
    "optimization": "optimization",
    "aws": "(amazon web services|aws)",
    "algorithms": "algorithms",
    "business_analyst": "(business analyst|ba)",
    "financial_analyst": "(financial analyst|financial analysis)",
    "operations_analyst": "operations analyst",
    "supply_chain_analyst": "supply chain analyst",
    "marketing_analyst": "marketing analyst",
    "product_analyst": "product analyst",
    "healthcare_analyst": "healthcare analyst",
    "hr_analyst": "(hr analyst|human resources analyst)",
    "sales_analyst": "sales analyst",
    "risk_analyst": "risk analyst",
    "quantitative_analyst": "quantitative analyst",
    "customer_success_analyst": "customer success analyst",
    "fraud_analyst": "fraud analyst",
    "logistics_analyst": "logistics analyst",
    "pricing_analyst": "pricing analyst",
    "portfolio_analyst": "portfolio analyst",
    "credit_analyst": "credit analyst",
    "cost_benefit_analysis": "cost[-\\s]?benefit analysis",
    "data_modeling": "data modeling",
    "data_quality": "data quality",
    "business_process": "business process",
    "business_requirements": "business requirements",
    "user_stories": "user stories",
    "scrum": "scrum",
    "business_strategy": "business strategy",
    "market_research": "market research",
    "competitive_analysis": "competitive analysis",
    "forecasting": "forecasting",
    "trend_analysis": "trend analysis",
    "budgeting": "budgeting",
    "profitability_analysis": "profitability analysis",
    "variance_analysis": "variance analysis",
    "six_sigma": "six sigma",
    "data_collection": "data collection",
    "data_interpretation": "data interpretation",
    "spreadsheets": "spreadsheets?",
    "siem": "siem",
    "ids": "ids",
    "firewall": "firewall",
    "wireshark": "wireshark",
    "splunk": "splunk",
    "qradar": "qradar",
    "edr": "edr",
    "soar": "soar",
    "incident_response": "incident response",
    "comptia": "comptia",
    "securityplus": "security\\+",
    "cysaplus": "cysa\\+",
    "velociraptor": "velociraptor",
    "soc_analyst": "soc analyst",
    "soc": "soc",
    "playbook": "playbook",
    "mitre_attack": "mitre att&ck",
    "cissp": "cissp",
    "gcih": "gcih",
    "gcfa": "gcfa",
    "gnfa": "gnfa",
    "grem": "grem",
    "aws_certified_cloud_practitioner": "aws certified cloud practitioner",
    "cyber_kill_chain": "cyber kill chain",
    "mcafee_nitro": "mcafee nitro",
    "unix": "unix",
    "active_directory": "active directory",
    "domain_controller": "domain controller",
    "office365": "office\\s?365",
    "ftp": "ftp",
    "http": "http",
    "ssh": "ssh",
    "smb": "smb",
    "dap": "dap",
    "ceh": "ceh",
    "splunk_search_processing_language": "splunk search processing language",
    "spl": "spl",
    "iec_iso_270000": "iec\\/iso 270000",
    "nist": "nist",
    "pci_dss": "pci dss",
    "cobit": "cobit",
    "soc2": "soc2",
    "cmmc": "cmmc",
    "itil": "itil",
    "windows_server_administration": "windows server administration",
    "lan_design": "lan design",
    "microsoft_active_directory": "microsoft active directory",
    "microsoft_azure_ad": "microsoft azure ad",
    "microsoft_azure_las": "microsoft azure las",
    "microsoft_o365_administration": "microsoft o365 administration",
    "workstation_support_virtualization": "workstation support virtualization",
    "vsphere": "vsphere",
    "hyperv": "hyper-v",
    "iso_iec_27001": "iso\\/iec 27001",
    "troubleshooting": "troubleshooting",
    "help_desk": "help\\s?desk",
    "technical_support": "technical support",
    "it_support": "it support",
    "remote_support": "remote support",
    "customer_support": "customer support",
    "networking": "networking",
    "windows": "windows",
    "macos": "mac\\s?os",
    "os_troubleshooting": "os troubleshooting",
    "hardware": "hardware",
    "itil_foundation": "itil foundation",
    "aplus": "a\\+",
    "networkplus": "network\\+",
    "voip": "voip",
    "cisco": "cisco",
    "ccna": "ccna",
    "ccnp": "ccnp",
    "ticketing_system": "ticketing system",
    "vmware": "vmware",
    "remote_desktop": "remote desktop",
    "teamviewer": "teamviewer",
    "anydesk": "anydesk",
    "antivirus": "antivirus",
    "malware_analysis": "malware analysis",
    "security_operations_center": "security operations center",
    "vulnerability_management": "vulnerability management",
    "threat_intelligence": "threat intelligence",
    "intrusion_detection": "intrusion detection",
    "intrusion_prevention": "intrusion prevention",
    "log_analysis": "log analysis",
    "security_event": "security event",
    "oscp": "oscp",
    "chfi": "chfi",
    "cisa": "cisa",
    "cism": "cism",
    "siem_administration": "siem administration",
    "first_tier_support": "first\\s?tier support",
    "tier_1_support": "tier\\s?1 support",
    "monitoring": "monitoring",
    "incident_detection": "incident detection",
    "incident_analysis": "incident analysis",
    "incident_handling": "incident handling"
}