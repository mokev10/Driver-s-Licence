
export const IIN_US: Record<string, string> = {
  "Alabama": "636033", "Alaska": "636059", "Arizona": "636026", "Arkansas": "636021", "California": "636014",
  "Colorado": "636020", "Connecticut": "636006", "Delaware": "636011", "Florida": "636010", "Georgia": "636055",
  "Hawaii": "636047", "Idaho": "636050", "Illinois": "636035", "Indiana": "636037", "Iowa": "636018",
  "Kansas": "636022", "Kentucky": "636046", "Louisiana": "636007", "Maine": "636041", "Maryland": "636003",
  "Massachusetts": "636002", "Michigan": "636032", "Minnesota": "636038", "Mississippi": "636051", "Missouri": "636030",
  "Montana": "636008", "Nebraska": "636054", "Nevada": "636049", "New Hampshire": "636039", "New Jersey": "636036",
  "New Mexico": "636009", "New York": "636001", "North Carolina": "636004", "North Dakota": "636034", "Ohio": "636023",
  "Oklahoma": "636058", "Oregon": "636029", "Pennsylvania": "636025", "Rhode Island": "636052", "South Carolina": "636005",
  "South Dakota": "636042", "Tennessee": "636053", "Texas": "636015", "Utah": "636040", "Vermont": "636024",
  "Virginia": "636000", "Washington": "636045", "West Virginia": "636061", "Wisconsin": "636031", "Wyoming": "636060"
};

export const IIN_CA: Record<string, string> = {
  "Alberta": "636031",
  "British Columbia": "636028",
  "Manitoba": "636030",
  "New Brunswick": "636027",
  "Newfoundland and Labrador": "636029",
  "Nova Scotia": "636025",
  "Ontario": "636032",
  "Prince Edward Island": "636026",
  "Quebec": "636033",
  "Saskatchewan": "636034"
};

export const CA_ABBR: Record<string, string> = {
  "Alberta": "AB",
  "British Columbia": "BC",
  "Manitoba": "MB",
  "New Brunswick": "NB",
  "Newfoundland and Labrador": "NL",
  "Nova Scotia": "NS",
  "Ontario": "ON",
  "Prince Edward Island": "PE",
  "Quebec": "QC",
  "Saskatchewan": "SK"
};

export const US_ABBR: Record<string, string> = {
  "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
  "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
  "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
  "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
  "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
  "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
  "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
  "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
  "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
  "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
};

export const US_STATES = Object.keys(IIN_US).sort();
export const CA_PROVINCES = Object.keys(IIN_CA).sort();

export const PREFIX_FIELDS = [
  { code: 'DCS', label: 'Last Name', help: 'SMITH' },
  { code: 'DAC', label: 'First Name', help: 'JOHN' },
  { code: 'DAD', label: 'Middle Name', help: 'QUINCY' },
  { code: 'DBB', label: 'Date of Birth', help: 'YYYY-MM-DD' },
  { code: 'DAG', label: 'Address', help: '123 MAIN ST' },
  { code: 'DAI', label: 'City', help: 'LOS ANGELES' },
  { code: 'DAJ', label: 'State/Prov', help: 'CA' },
  { code: 'DAK', label: 'Zip', help: '90001' },
  { code: 'DBD', label: 'Issue Date', help: 'YYYY-MM-DD' },
  { code: 'DBA', label: 'Expiry Date', help: 'YYYY-MM-DD' },
  { code: 'DBC', label: 'Sex', help: '1=M, 2=F' },
  { code: 'DAY', label: 'Eye Color', help: 'BRN' },
  { code: 'DAU', label: 'Height', help: '5-10' },
  { code: 'DCF', label: 'DL Number', help: 'F1234567' },
];

export const CANADA_EXAMPLE: Record<string, string> = {
  DCS: 'TRUDEAU',
  DAC: 'JUSTIN',
  DAI: 'OTTAWA',
  DAJ: 'ON',
};
