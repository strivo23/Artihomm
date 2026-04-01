import os
files = {}

files['src/pages/Home.css'] = """
/* ── SECTION BASE ── */
section { padding:5rem 5vw; border-top:1px solid var(--border); }
.section-label {
  font-size:.68rem; font-weight:600; letter-spacing:.14em;
  text-transform:uppercase; color:var(--gold); margin-bottom:.9rem;
}
.section-title {
  font-family:var(--serif); font-size:clamp(1.9rem,4vw,2.8rem);
  font-weight:600; color:var(--cream); line-height:1.12;
  margin-bottom:.8rem; letter-spacing:-.01em;
}
.section-sub { font-size:.97rem; color:var(--muted); line-height:1.82; max-width:520px; }
.gold-rule { width:40px; height:2px; background:linear-gradient(90deg, var(--gold), transparent); margin:1.2rem 0 1.8rem; }

/* ── HERO ── */
#hero {
  min-height:100svh; display:flex; flex-direction:column; justify-content:flex-end;
  padding:6rem 5vw 4rem; position:relative; overflow:hidden;
  background: radial-gradient(ellipse 80% 60% at 50% -10%, rgba(200,169,106,.09) 0%, transparent 65%), var(--bg);
}
.hero-grid-bg {
  position:absolute; inset:0; pointer-events:none;
  background-image: linear-gradient(rgba(200,169,106,.03) 1px, transparent 1px), linear-gradient(90deg, rgba(200,169,106,.03) 1px, transparent 1px);
  background-size:56px 56px;
}
.hero-vignette { position:absolute; inset:0; pointer-events:none; background:radial-gradient(ellipse 100% 100% at 50% 50%, transparent 40%, rgba(9,9,10,.7) 100%); }
.hero-badge {
  display:inline-flex; align-items:center; gap:.45rem;
  background:rgba(200,169,106,.07); border:1px solid rgba(200,169,106,.2);
  border-radius:20px; padding:.32rem .9rem;
  font-size:.7rem; font-weight:600; color:var(--glow); letter-spacing:.06em;
  margin-bottom:1.8rem; width:fit-content;
}
.hero-badge .dot { width:6px; height:6px; border-radius:50%; background:var(--green); animation:pulse 2s infinite; }
.hero-h1 { font-family:var(--serif); font-size:clamp(2.8rem,8vw,5.6rem); font-weight:600; line-height:1.02; letter-spacing:-.02em; color:var(--cream); margin-bottom:1.6rem; }
.hero-sub-text { font-size:clamp(.95rem,2.5vw,1.08rem); color:var(--text); line-height:1.85; max-width:500px; margin-bottom:2.4rem; }
.hero-btns { display:flex; gap:.85rem; flex-wrap:wrap; margin-bottom:2.8rem; }

/* ── CATALOGUE ── */
#catalogue { background:var(--bg); }
.cat-tabs { display:flex; gap:.5rem; flex-wrap:wrap; margin:1.8rem 0 2rem; }
.cat-tab {
  background:transparent; border:1px solid var(--border); color:var(--muted);
  padding:.42rem 1rem; border-radius:20px; font-size:.78rem; font-weight:500; transition:all .2s;
}
.cat-tab.active, .cat-tab:hover { background:rgba(200,169,106,.1); border-color:rgba(200,169,106,.4); color:var(--cream); }
.products-grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(260px,1fr)); gap:1.2rem; }

/* ── HOW IT WORKS & WHY US ── */
#how, #why { background:var(--surface); }
.steps-grid, .why-grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(260px,1fr)); gap:1.2rem; margin-top:3rem; }
.step-card, .why-card {
  background:var(--bg); border:1px solid var(--border); border-radius:14px; padding:1.6rem 1.5rem;
  transition:border-color .25s, transform .25s; position:relative; overflow:hidden;
}
.step-card::after { content:''; position:absolute; inset:0; pointer-events:none; background:linear-gradient(135deg, rgba(200,169,106,.03) 0%, transparent 60%); }
.step-card:hover, .why-card:hover { border-color:rgba(200,169,106,.35); transform:translateY(-3px); }
.step-num { font-family:var(--serif); font-size:3rem; font-weight:700; color:var(--dim); line-height:1; margin-bottom:1rem; background:linear-gradient(90deg, var(--gold), transparent); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.step-icon, .why-icon { width:40px; height:40px; border-radius:10px; background:rgba(200,169,106,.07); border:1px solid rgba(200,169,106,.15); display:flex; align-items:center; justify-content:center; margin-bottom:1rem; }
.step-title, .why-title { font-family:var(--serif); font-size:1.12rem; font-weight:600; color:var(--cream); margin-bottom:.4rem; }
.step-desc, .why-desc { font-size:.84rem; color:var(--muted); line-height:1.7; }

/* ── COST COMPARISON ── */
#compare { background:var(--bg); }
.compare-bars { margin-top:2.8rem; display:flex; flex-direction:column; gap:1.4rem; }
.compare-labels { display:flex; justify-content:space-between; margin-bottom:.5rem; }
.compare-label { font-size:.8rem; color:var(--text); }
.compare-amount { font-size:.8rem; font-weight:600; }
.bar-track { height:8px; background:var(--border); border-radius:10px; overflow:hidden; position:relative; }
.bar-fill { height:100%; border-radius:10px; transition:width 1.2s cubic-bezier(.22,1,.36,1); }

/* ── INTEREST POLL ── */
#poll { background:var(--surface); }
.poll-options { display:flex; flex-direction:column; gap:.85rem; margin-top:2rem; }
.poll-option {
  background:var(--bg); border:1.5px solid var(--border); border-radius:10px; padding:1rem 1.2rem;
  display:flex; align-items:center; gap:1rem; cursor:pointer; transition:all .22s;
}
.poll-option:hover { border-color:rgba(200,169,106,.35); }
.poll-radio { width:18px; height:18px; border-radius:50%; border:1.5px solid var(--muted); flex-shrink:0; display:flex; align-items:center; justify-content:center; }
.poll-radio-dot { width:9px; height:9px; border-radius:50%; background:var(--gold); opacity:0; transition:opacity .2s; }
.poll-option.selected .poll-radio { border-color:var(--gold); }
.poll-option.selected .poll-radio-dot { opacity:1; }
.poll-label { font-size:.9rem; color:var(--text); flex:1; }
.poll-option.selected .poll-label { color:var(--cream); }
.poll-bar-row { margin-bottom:.7rem; }
.poll-bar-labels { display:flex; justify-content:space-between; margin-bottom:.35rem; }
.poll-bar-text { font-size:.78rem; color:var(--muted); }
.poll-bar-pct { font-size:.78rem; font-weight:600; color:var(--gold); }
.poll-track { height:6px; background:var(--border); border-radius:6px; overflow:hidden; }
.poll-fill { height:100%; background:var(--gold); border-radius:6px; width:0; transition:width 1s ease; }

/* ── FOOTER ── */
footer { border-top:1px solid var(--border); padding:2.5rem 5vw; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:1rem; }
.footer-logo { font-family:var(--serif); font-size:1.2rem; font-weight:600; color:var(--cream); }
.footer-logo span { color:var(--gold); }
.footer-text { font-size:.78rem; color:var(--muted); }
.footer-socials { display:flex; gap:.75rem; }
.footer-social { width:34px; height:34px; border-radius:8px; border:1px solid var(--border); display:flex; align-items:center; justify-content:center; background:transparent; color:var(--muted); transition:all .2s; }
.footer-social:hover { border-color:rgba(200,169,106,.4); color:var(--gold); }

@media(max-width:600px) { footer { flex-direction:column; text-align:center; } }
"""

files['src/pages/Home.jsx'] = """import React, { useState, useEffect, useRef, useContext } from 'react';
import { Link } from 'react-router-dom';
import ProductCard from '../components/ProductCard';
import WaitlistModal from '../components/WaitlistModal';
import { AuthContext } from '../context/AuthContext';
import { getProducts } from '../api';
import './Home.css';

const TABS = ['All', 'Sofa', 'Bed', 'Table', 'Chair', 'Storage'];

function Home() {
  const { isLoggedIn } = useContext(AuthContext);
  const [activeTab, setActiveTab] = useState('All');
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [waitlistProduct, setWaitlistProduct] = useState(null);

  // Poll state
  const [voted, setVoted] = useState(false);
  const [pollVotes] = useState([52, 28, 14, 6]);

  const barsRef = useRef(null);

  useEffect(() => {
    // Fetch products
    setLoading(true);
    getProducts(activeTab).then(res => {
      setProducts(res.data);
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, [activeTab]);

  useEffect(() => {
    // Intersection Observer for animations
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if(e.isIntersecting) {
          e.target.classList.add('visible');
          if (e.target.id === 'cost-bars') {
             const fills = e.target.querySelectorAll('.bar-fill');
             fills.forEach(bar => { bar.style.width = bar.dataset.width; });
          }
        }
      });
    }, { threshold: .12 });
    
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
    if (barsRef.current) observer.observe(barsRef.current);

    return () => observer.disconnect();
  }, []);

  const handleVote = (idx) => {
    if (voted) return;
    setVoted(true);
    // Poll percentage logic
    setTimeout(() => {
        document.querySelectorAll('.poll-fill').forEach(f => {
            f.style.width = f.dataset.w;
        });
    }, 100);
  };

  const pollLabels = [
    "Yes — ordering right now",
    "Probably — need more info",
    "Maybe — depends on quality",
    "No — prefer in-store"
  ];
  const totalVotes = pollVotes.reduce((a,b) => a+b, 0) + (voted ? 1 : 0);

  return (
    <div>
      <section id="hero">
        <div className="hero-grid-bg"></div>
        <div className="hero-vignette"></div>
        <div style={{position:'relative'}}>
          <div className="hero-badge"><span className="dot"></span>DEMAND VALIDATION · PHASE 1</div>
          <h1 className="hero-h1">Premium sofas.<br/><span className="shimmer-text">Half the price.</span></h1>
          <div className="gold-rule"></div>
          <p className="hero-sub-text">
            ArtiHome connects you directly to vetted local welders, carpenters & tailors — no factory, no showroom, no middleman markup.
          </p>
          <div className="hero-btns">
            <button className="btn-primary" onClick={() => document.getElementById('catalogue').scrollIntoView({behavior:'smooth'})}>
              Browse & Join Waitlist
            </button>
            <button className="btn-ghost" onClick={() => document.getElementById('how').scrollIntoView({behavior:'smooth'})}>
              How it works
            </button>
          </div>
          <p style={{fontSize:'.82rem', color:'var(--muted)'}}><strong>140+ people</strong> have already expressed interest</p>
        </div>
      </section>

      <section id="how">
        <div className="reveal">
          <p className="section-label">The Process</p>
          <h2 className="section-title">No factory needed.<br/>Just skilled hands.</h2>
        </div>
        <div className="steps-grid">
          {['You Order Online', 'Platform Assigns', 'Crafted Locally', 'Delivered to You'].map((title, i) => (
             <div className="step-card reveal" style={{transitionDelay: `${i*0.06}s`}} key={i}>
                <div className="step-num">0{i+1}</div>
                <p className="step-title">{title}</p>
                <p className="step-desc">Direct-to-home model cuts middlemen and saves you money while empowering artisans.</p>
             </div>
          ))}
        </div>
      </section>

      <section id="catalogue">
        <div className="reveal">
          <p className="section-label">The Collection</p>
          <h2 className="section-title">Every piece,<br/><em style={{fontStyle:'italic', color:'var(--gold)'}}>honestly priced.</em></h2>
        </div>
        
        <div className="cat-tabs reveal">
          {TABS.map(tab => (
             <button key={tab} className={`cat-tab ${activeTab === tab ? 'active' : ''}`} onClick={() => setActiveTab(tab)}>
               {tab}
             </button>
          ))}
        </div>

        {loading ? (
            <p style={{color:'var(--muted)'}}>Loading catalogue...</p>
        ) : (
            <div className="products-grid">
              {products.map((p, idx) => (
                 <ProductCard key={p.id} product={p} index={idx} onJoinWaitlist={setWaitlistProduct} />
              ))}
            </div>
        )}
      </section>

      <section id="why">
        <div className="reveal"><p className="section-label">Why ArtiHome</p><h2 className="section-title">Cut out everything<br/>that drives up cost.</h2></div>
        <div className="why-grid">
           {['No Showroom Markup', 'Vetted Local Artisans', '1-Year Warranty', 'Swappable Covers', '7–10 Day Delivery', 'Jobs for Local Craftsmen'].map((w,i)=>(
             <div className="why-card reveal" style={{transitionDelay:`${i*0.06}s`}} key={i}>
                <p className="why-title">{w}</p>
             </div>
           ))}
        </div>
      </section>

      <section id="compare">
        <div className="reveal">
           <p className="section-label">Transparent Pricing</p>
           <h2 className="section-title">Where does the money go?</h2>
        </div>
        <div className="compare-bars reveal" id="cost-bars" ref={barsRef} style={{maxWidth:'560px', marginTop:'2.8rem'}}>
           {[
             {name: "Iron Frame + Labour", price: "Rs. 6,000", w: "33%", c: "#8A6A10"},
             {name: "High-Density Foam", price: "Rs. 4,000", w: "22%", c: "var(--gold)"},
             {name: "Fabric & Stitching", price: "Rs. 3,000", w: "17%", c: "#C9A84C"},
             {name: "Platform + Our Profit", price: "Rs. 5,000", w: "28%", c: "var(--green)"}
           ].map((b,i) => (
              <div key={i}>
                <div className="compare-labels"><span className="compare-label">{b.name}</span><span className="compare-amount" style={{color:b.c}}>{b.price}</span></div>
                <div className="bar-track"><div className="bar-fill" data-width={b.w} style={{background: b.c, width:0}}></div></div>
              </div>
           ))}
           <div style={{marginTop:'1.8rem', padding:'1.2rem', background:'rgba(200,169,106,.06)', border:'1px solid rgba(200,169,106,.18)', borderRadius:'10px', display:'flex', justifyContent:'space-between'}}>
              <div><p style={{fontSize:'.74rem',color:'var(--muted)'}}>ArtiHome Total</p><p style={{fontFamily:'var(--serif)',fontSize:'1.5rem',fontWeight:'700',color:'var(--gold)'}}>Rs. 18,000</p></div>
              <div style={{textAlign:'right'}}><p style={{fontSize:'.74rem',color:'var(--muted)'}}>Showroom charges</p><p style={{fontFamily:'var(--serif)',fontSize:'1.5rem',fontWeight:'700',color:'var(--text)',textDecoration:'line-through',opacity:'.6'}}>Rs. 42,000</p></div>
           </div>
        </div>
      </section>

      <section id="poll">
        <div className="reveal">
          <p className="section-label">Quick Poll</p>
          <h2 className="section-title">Would you buy from ArtiHome?</h2>
        </div>
        <div style={{maxWidth:'480px', marginTop:'2rem'}}>
          {!voted ? (
            <div className="poll-options reveal">
              {pollLabels.map((lbl, idx) => (
                <div className="poll-option" key={idx} onClick={() => handleVote(idx)}>
                  <div className="poll-radio"><div className="poll-radio-dot"></div></div>
                  <span className="poll-label">{lbl}</span>
                </div>
              ))}
            </div>
          ) : (
            <div className="reveal">
              <p style={{fontSize:'.82rem',color:'var(--muted)',marginBottom:'1.2rem'}}>Based on {totalVotes} responses</p>
              {pollVotes.map((v,i) => {
                const pct = Math.round(((v + (i===0?1:0))/totalVotes)*100);
                return (
                  <div className="poll-bar-row" key={i}>
                    <div className="poll-bar-labels"><span className="poll-bar-text">{pollLabels[i]}</span><span className="poll-bar-pct">{pct}%</span></div>
                    <div className="poll-track"><div className="poll-fill" data-w={`${pct}%`} style={{width:0}}></div></div>
                  </div>
                );
              })}
              <div style={{textAlign:'center', marginTop:'2rem'}}>
                <div style={{fontSize:'2.5rem'}}>🙏</div><p className="section-title" style={{fontSize:'1.5rem'}}>Thank you!</p>
              </div>
            </div>
          )}
        </div>
      </section>

      <section style={{textAlign:'center', background:'radial-gradient(ellipse 80% 60% at 50% 50%, rgba(200,169,106,.08) 0%, transparent 70%), var(--surface)'}}>
        <div className="reveal">
           <h2 className="section-title" style={{margin:'0 auto 2rem'}}>Stop paying the showroom tax.</h2>
           {isLoggedIn ? (
             <button className="btn-primary" onClick={() => document.getElementById('catalogue').scrollIntoView()}>Browse Products</button>
           ) : (
             <div style={{display:'flex', gap:'1rem', justifyContent:'center'}}>
               <Link to="/register" className="btn-primary">Create Account</Link>
               <Link to="/login" className="btn-ghost">Login</Link>
             </div>
           )}
        </div>
      </section>

      <footer>
        <p className="footer-logo">Arti<span>Home</span></p>
        <p className="footer-text">© 2026 ArtiHome. Direct-to-home furniture.</p>
        <div className="footer-socials">
          <div className="footer-social">IG</div><div className="footer-social">FB</div><div className="footer-social">WA</div>
        </div>
      </footer>

      {waitlistProduct && <WaitlistModal product={waitlistProduct} onClose={() => setWaitlistProduct(null)} />}
    </div>
  );
}

export default Home;
"""

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
