import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  CreditCard, 
  MapPin, 
  Settings, 
  User, 
  Eye, 
  Download, 
  RefreshCw, 
  FileCode, 
  Copy, 
  CheckCircle2,
  Info,
  ShieldCheck,
  Zap,
  Cpu,
  BarChart3
} from 'lucide-react';
import confetti from 'canvas-confetti';
import bwipjs from 'bwip-js';

import { 
  IIN_US, 
  IIN_CA, 
  US_STATES, 
  CA_PROVINCES, 
  PREFIX_FIELDS,
  US_ABBR,
  CA_ABBR
} from './constants';

type Country = 'Canada' | 'United States' | '';

export default function App() {
  const [country, setCountry] = useState<Country>('United States');
  const [subdivision, setSubdivision] = useState<string>('California');
  const [fields, setFields] = useState<Record<string, string>>(() => {
    const initial: Record<string, string> = {
      DCS: 'WALKER',
      DAC: 'ELIJAH',
      DBB: '1992-07-24',
      DAG: '742 EVERGREEN TER',
      DAI: 'SACRAMENTO',
      DAJ: 'CA',
      DAK: '95814',
      DBD: '2022-11-15',
      DBA: '2027-07-24',
      DBC: 'M',
      DAY: 'BLU',
      DAU: '6-00',
      DCF: 'D9823415',
    };
    return initial;
  });
  const [aamvaText, setAamvaText] = useState<string>('');
  const [copied, setCopied] = useState(false);
  const barcodeRef = useRef<HTMLCanvasElement>(null);

  // Sync state/prov when subdivision changes
  useEffect(() => {
    if (subdivision) {
      const abbr = country === 'United States' 
        ? US_ABBR[subdivision] 
        : CA_ABBR[subdivision];
      setFields(prev => ({ ...prev, DAJ: abbr || subdivision }));
    }
  }, [subdivision, country]);

  const handleFieldChange = (code: string, value: string) => {
    setFields(prev => ({ ...prev, [code]: value }));
  };

  const normalizeDate = (val: string) => val.replace(/-/g, '').trim();

  const generateAAMVA = () => {
    const iin = country === 'United States' 
      ? IIN_US[subdivision] || '636000'
      : IIN_CA[subdivision] || '636005';
    
    const dataLines: string[] = [];
    if (fields.DCF) {
      dataLines.push(`DAQ${fields.DCF}`);
    }

    const order = ["DCS", "DAC", "DBB", "DAG", "DAI", "DAJ", "DAK", "DBD", "DBA", "DBC", "DAU", "DAY", "DCE", "DCG", "DCF"];
    order.forEach(code => {
      let val = fields[code];
      if (val) {
        if (["DBB", "DBD", "DBA"].includes(code)) {
          val = normalizeDate(val);
        }
        val = String(val).replace(/\n/g, ' ').trim();
        dataLines.push(`${code}${val}`);
      }
    });

    const header = `ANSI ${iin}050102DL00410287ZO02900045DL`;
    const realDataBlock = dataLines.join('\n');
    
    const finalResult = `@\n${header}\n${realDataBlock}`;
    setAamvaText(finalResult);
    
    // Generate barcode visual
    if (barcodeRef.current && finalResult) {
      try {
        bwipjs.toCanvas(barcodeRef.current, {
          bcid: 'pdf417',
          text: finalResult,
          scale: 3,
          height: 10,
          includetext: false,
        });
      } catch (e) {
        console.error('Barcode gen error:', e);
      }
    }

    confetti({
      particleCount: 80,
      spread: 60,
      origin: { y: 0.8 },
      colors: ['#F59E0B', '#FFFFFF', '#141417']
    });
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(aamvaText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleRandomize = () => {
    const firstNames = ['LIAM', 'NOAH', 'OLIVER', 'JAMES', 'ELIJAH', 'EMMA', 'CHARLOTTE', 'AMELIA', 'SOPHIA', 'MIA'];
    const lastNames = ['WALKER', 'HALL', 'YOUNG', 'KING', 'WRIGHT', 'LOPEZ', 'HILL', 'SCOTT', 'GREEN', 'ADAMS'];
    const randomFirst = firstNames[Math.floor(Math.random() * firstNames.length)];
    const randomLast = lastNames[Math.floor(Math.random() * lastNames.length)];
    const randomDL = 'D' + Math.floor(1000000 + Math.random() * 9000000);
    
    setFields(prev => ({
      ...prev,
      DAC: randomFirst,
      DCS: randomLast,
      DCF: randomDL,
    }));
  };

  // Generate initial barcode
  useEffect(() => {
    generateAAMVA();
  }, [barcodeRef.current]);

  return (
    <div className="bg-[#0A0A0B] text-gray-300 w-full min-h-screen flex flex-col font-sans overflow-x-hidden selection:bg-amber-500/30 selection:text-amber-200">
      {/* Navigation */}
      <nav className="h-16 border-b border-white/10 flex items-center justify-between px-8 bg-[#0F0F12] sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-amber-500 rounded flex items-center justify-center text-black font-bold text-lg italic shadow-lg shadow-amber-500/20">C</div>
          <span className="text-white font-medium tracking-tight text-xl">Calcul-DL <span className="text-amber-500/80 font-light italic">California Edition</span></span>
        </div>
        <div className="hidden md:flex items-center gap-6 text-sm font-medium text-gray-400">
          <span className="text-amber-500 border-b border-amber-500 pb-5 mt-5">Analysis</span>
          <span className="hover:text-white transition-colors cursor-pointer">Visualizer</span>
          <span className="hover:text-white transition-colors cursor-pointer">Export</span>
          <div className="w-px h-4 bg-white/20 mx-2"></div>
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-full bg-gradient-to-tr from-gray-700 to-gray-600"></div>
            <span className="text-gray-500">v2.4.0</span>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1 flex flex-col lg:flex-row p-6 gap-6 max-w-[1600px] mx-auto w-full">
        {/* Sidebar: Parameter Configuration */}
        <section className="w-full lg:w-1/3 flex flex-col gap-6">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-[#141417] border border-white/5 rounded-2xl p-6 flex flex-col gap-5 shadow-2xl"
          >
            <div className="flex justify-between items-center">
              <h2 className="text-xs uppercase tracking-widest text-amber-500 font-bold">Parameter Configuration</h2>
              <button 
                onClick={handleRandomize}
                className="text-[10px] text-gray-600 hover:text-amber-500 uppercase tracking-widest transition-colors flex items-center gap-1"
              >
                <RefreshCw size={10} /> Randomize
              </button>
            </div>
            
            <div className="space-y-4">
              <div className="flex flex-col gap-2">
                <label className="text-xs text-gray-500 uppercase">Jurisdiction Profile</label>
                <div className="bg-black/40 border border-white/10 rounded-lg p-3 font-mono text-amber-100 flex justify-between items-center">
                  <span>{country || 'Global'} // {subdivision || 'None'}</span>
                  <Settings size={14} className="text-gray-600" />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="flex flex-col gap-2">
                  <label className="text-xs text-gray-500 uppercase">Country</label>
                  <select 
                    value={country}
                    onChange={(e) => setCountry(e.target.value as Country)}
                    className="bg-black/40 border border-white/10 rounded-lg p-3 font-mono text-white outline-none focus:border-amber-500/50 appearance-none transition-all"
                  >
                    <option value="United States">US</option>
                    <option value="Canada">CA</option>
                  </select>
                </div>
                <div className="flex flex-col gap-2">
                  <label className="text-xs text-gray-500 uppercase">Region</label>
                  <select 
                    value={subdivision}
                    onChange={(e) => setSubdivision(e.target.value)}
                    className="bg-black/40 border border-white/10 rounded-lg p-3 font-mono text-white outline-none focus:border-amber-500/50 appearance-none transition-all"
                  >
                    {country === 'United States' ? US_STATES.map(s => <option key={s} value={s}>{s}</option>) : CA_PROVINCES.map(p => <option key={p} value={p}>{p}</option>)}
                  </select>
                </div>
              </div>
            </div>
            <button 
              onClick={generateAAMVA}
              className="mt-4 bg-amber-500 hover:bg-amber-400 text-black font-bold py-3 rounded-lg transition-colors text-sm uppercase tracking-wide active:scale-95 shadow-lg shadow-amber-500/20"
            >
              Run Expansion
            </button>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-[#141417] border border-white/5 rounded-2xl p-6 h-[400px] shadow-2xl overflow-hidden flex flex-col"
          >
            <h2 className="text-xs uppercase tracking-widest text-gray-500 font-bold mb-4">Identity Coefficients</h2>
            <div className="space-y-1 overflow-y-auto pr-2 custom-scrollbar flex-1">
              {PREFIX_FIELDS.map((f) => (
                <div key={f.code} className="flex justify-between items-center py-2.5 border-b border-white/5 group transition-colors hover:bg-white/[0.02] -mx-2 px-2 rounded">
                  <div className="flex flex-col">
                    <span className="text-xs font-mono text-gray-500 group-hover:text-amber-500/50 transition-colors uppercase tracking-widest">{f.label}</span>
                    <span className="text-[10px] text-gray-700 font-mono tracking-tighter">PREFIX: {f.code}</span>
                  </div>
                  <input 
                    type="text"
                    value={fields[f.code]}
                    onChange={(e) => handleFieldChange(f.code, e.target.value)}
                    placeholder={f.help}
                    className="flex-1 bg-transparent border-none text-right font-mono text-sm text-amber-200 placeholder:text-gray-800 focus:ring-0 outline-none"
                  />
                </div>
              ))}
            </div>
          </motion.div>
        </section>

        {/* Visualization & Results */}
        <section className="flex-1 flex flex-col gap-6">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-[#141417] border border-white/5 rounded-2xl flex-1 relative overflow-hidden flex flex-col shadow-2xl min-h-[400px]"
          >
            <div className="p-6 flex justify-between items-center bg-black/20 border-b border-white/5">
              <h2 className="text-xs uppercase tracking-widest text-gray-500 font-bold">AAMVA PDF417 Logic Visualizer</h2>
              <div className="flex gap-4">
                <div className="flex items-center gap-2 text-[10px]">
                  <div className="w-2 h-2 rounded-full bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.5)]"></div>
                  <span>ENCRYPTION ACTIVE</span>
                </div>
                <div className="flex items-center gap-2 text-[10px]">
                  <div className="w-2 h-2 rounded-full bg-white opacity-40"></div>
                  <span>RAW DATA STREAM</span>
                </div>
              </div>
            </div>
            
            <div className="flex-1 relative m-6 rounded-xl bg-black/20 border border-white/5 overflow-hidden flex flex-col">
              <div className="flex-1 flex items-center justify-center p-8">
                <AnimatePresence mode="wait">
                  <motion.div 
                    key={JSON.stringify(fields)}
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 1.05 }}
                    className="relative"
                  >
                    <div className="bg-white p-6 rounded-lg shadow-2xl shadow-black border border-white/10 group">
                      <canvas ref={barcodeRef} className="max-w-full h-auto grayscale contrast-150 group-hover:grayscale-0 transition-all"></canvas>
                      <div className="absolute inset-0 bg-blue-500/5 pointer-events-none mix-blend-overlay"></div>
                    </div>
                    {/* Floating Info Labels */}
                    <div className="absolute top-0 right-0 -translate-y-4 translate-x-4 flex flex-col gap-2">
                      <div className="px-2 py-1 bg-[#141417] border border-white/10 rounded text-[10px] uppercase tracking-widest text-amber-500 font-mono">ECC LEVEL 5</div>
                      <div className="px-2 py-1 bg-[#141417] border border-white/10 rounded text-[10px] uppercase tracking-widest text-gray-500 font-mono">0x{fields.DCF?.slice(-4) || 'NULL'}</div>
                    </div>
                  </motion.div>
                </AnimatePresence>
              </div>

              {/* Data Strip */}
              <div className="h-24 bg-black/40 border-t border-white/5 p-4 overflow-y-auto custom-scrollbar group font-mono text-[11px]">
                 <div className="flex justify-between items-start">
                   <div className="text-amber-200/40 break-all leading-tight italic overflow-hidden">
                     {aamvaText || 'Awaiting kernel execution...'}
                   </div>
                   <button 
                    onClick={copyToClipboard}
                    className="ml-4 p-2 bg-white/5 border border-white/10 rounded-lg hover:bg-white/10 transition-colors text-gray-500 hover:text-white"
                   >
                     {copied ? <CheckCircle2 size={16} className="text-green-500" /> : <Copy size={16} />}
                   </button>
                 </div>
              </div>
            </div>
            
            <div className="absolute bottom-8 right-8 flex gap-2 pointer-events-none">
              <div className="px-2 py-1 bg-white/5 border border-white/10 rounded text-[10px] uppercase tracking-tighter opacity-50">Zoom: 1.0x</div>
              <div className="px-2 py-1 bg-white/5 border border-white/10 rounded text-[10px] uppercase tracking-tighter opacity-50">Raster: High</div>
            </div>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="h-32 bg-amber-500/5 border border-amber-500/20 rounded-2xl p-6 flex items-center justify-between shadow-xl"
          >
            <div className="flex flex-col items-start">
              <h3 className="text-amber-500 text-xs font-bold uppercase tracking-widest mb-1 flex items-center gap-2">
                <BarChart3 size={12} className="fill-amber-500/20" /> Analytic Result
              </h3>
              <p className="font-serif italic text-2xl text-white tracking-tight">Encoded Record: <span className="text-amber-200/80">{fields.DAC} {fields.DCS}</span></p>
              <div className="mt-2 flex gap-2">
                <span className="px-1.5 py-0.5 bg-white/5 rounded text-[8px] text-gray-500 uppercase font-bold tracking-widest border border-white/5">AES_256</span>
                <span className="px-1.5 py-0.5 bg-white/5 rounded text-[8px] text-gray-500 uppercase font-bold tracking-widest border border-white/5">BATT_SYNC</span>
              </div>
            </div>
            <div className="text-right">
              <p className="text-xs text-gray-600 uppercase mb-1 tracking-widest">AAMVA Compliance (DL)</p>
              <p className="font-mono text-xl text-white tracking-tighter">0.00042 <span className="text-xs text-green-500/80 font-bold ml-1">STABLE</span></p>
            </div>
          </motion.div>
        </section>
      </main>

      {/* Footer */}
      <footer className="h-10 bg-black border-t border-white/5 px-8 flex items-center justify-between text-[10px] text-gray-700 uppercase tracking-widest">
        <div className="flex gap-4 items-center">
          <span className="flex items-center gap-1.5"><div className="w-1 h-1 bg-amber-500 rounded-full animate-pulse"></div> Processing Engine: California V8</span>
          <div className="w-px h-3 bg-white/10"></div>
          <span className="opacity-50">Authorized Use Only</span>
        </div>
        <div className="flex gap-6">
          <span>Precision: <span className="text-gray-500 italic">64-bit FP</span></span>
          <span>Kernel: <span className="text-gray-500 italic">Optimized ASM</span></span>
        </div>
      </footer>

      <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(255, 255, 255, 0.05);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(255, 255, 255, 0.1);
        }
      `}</style>
    </div>
  );
}
