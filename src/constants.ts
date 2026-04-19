
export const IIN_US: Record<string, string> = {
  'California': '636000',
  'New York': '636001',
  'Texas': '636002',
  'Florida': '636003',
  'Washington': '636004',
};

export const IIN_CA: Record<string, string> = {
  'Ontario': '636005',
  'Quebec': '636006',
  'British Columbia': '636007',
  'Alberta': '636008',
};

export const CA_ABBR: Record<string, string> = {
  'Ontario': 'ON',
  'Quebec': 'QC',
  'British Columbia': 'BC',
  'Alberta': 'AB',
};

export const US_STATES = Object.keys(IIN_US);
export const CA_PROVINCES = Object.keys(IIN_CA);

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
  { code: 'DBC', label: 'Sex', help: 'M/F' },
  { code: 'DAY', label: 'Eye Color', help: 'BRN' },
  { code: 'DAU', label: 'Height', help: '5-10' },
  { code: 'DCF', label: 'DL Number', help: 'F1234567' },
];

export const CANADA_EXAMPLE: Record<string, string> = {
  DCS: 'TRUDEAU',
  DAC: 'JUSTIN',
  DAI: 'OTTAWA',
  DAJ: 'ON',
  DCG: 'CAN',
};
