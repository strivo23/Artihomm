import React, { useState, useEffect, useRef, useContext } from 'react';
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
      if (import.meta.env.DEV) {
        console.error(err);
      }
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
  }, [products.length]);

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
              <div style={{textAlign:'center', marginBottom:'2.4rem'}}>
                <div style={{fontSize:'3rem', marginBottom:'0.8rem'}}>🙏</div>
                <p className="section-title" style={{fontSize:'1.8rem', marginBottom:'0.5rem'}}>Thank you for voting!</p>
                <p style={{fontSize:'.82rem',color:'var(--muted)'}}>Here's what {totalVotes} people think:</p>
              </div>
              {pollVotes.map((v,i) => {
                const pct = Math.round(((v + (i===0?1:0))/totalVotes)*100);
                return (
                  <div className="poll-bar-row" key={i}>
                    <div className="poll-bar-labels"><span className="poll-bar-text">{pollLabels[i]}</span><span className="poll-bar-pct">{pct}%</span></div>
                    <div className="poll-track"><div className="poll-fill" data-w={`${pct}%`} style={{width:0}}></div></div>
                  </div>
                );
              })}
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
