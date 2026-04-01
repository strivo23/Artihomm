import os
files = {}

files['src/components/ProductCard.css'] = """
.product-card {
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:14px; overflow:hidden;
  transition:all .25s; cursor:pointer;
  display:flex; flex-direction:column;
}
.product-card:hover {
  border-color:rgba(200,169,106,.4);
  transform:translateY(-4px);
  box-shadow:0 16px 40px rgba(0,0,0,.45);
}
.product-img {
  height:180px; position:relative; overflow:hidden;
  background:var(--border);
}
.product-img img {
  width:100%; height:100%; object-fit:cover;
  transition:transform .4s;
}
.product-card:hover .product-img img { transform:scale(1.06); }
.product-img-overlay {
  position:absolute; inset:0;
  background:linear-gradient(180deg, rgba(0,0,0,.22) 0%, transparent 45%, rgba(0,0,0,.15) 100%);
}
.product-tag {
  position:absolute; top:10px; left:10px; z-index:2;
  background:rgba(200,169,106,.15);
  border:1px solid rgba(200,169,106,.35);
  color:var(--gold); font-size:.62rem; font-weight:600;
  letter-spacing:.1em; text-transform:uppercase;
  padding:.26rem .7rem; border-radius:12px;
}
.product-body { padding:1.1rem 1.15rem; flex:1; display:flex; flex-direction:column; }
.product-name {
  font-family:var(--serif);
  font-size:1.05rem; font-weight:600; color:var(--cream);
  line-height:1.25; margin-bottom:.3rem;
}
.product-sub { font-size:.76rem; color:var(--muted); line-height:1.55; flex:1; }
.product-prices {
  display:flex; align-items:baseline; gap:.5rem;
  margin-top:.85rem; flex-wrap:wrap;
}
.price-ah {
  font-family:var(--serif);
  font-size:1.22rem; font-weight:700; color:var(--gold);
}
.price-mkt {
  font-size:.75rem; color:var(--muted);
  text-decoration:line-through;
}
.price-save {
  font-size:.72rem; font-weight:700; color:var(--green);
  margin-left:auto;
}

/* ── CARD ACTIONS ── */
.product-footer {
  display:flex; flex-direction:column;
  gap:.75rem; margin-top:.85rem;
}
.card-actions {
  display:grid; grid-template-columns:1fr 1fr; gap:.5rem;
}
.btn-card-waitlist {
  display:inline-flex; align-items:center; justify-content:center; gap:.35rem;
  background:rgba(200,169,106,.1);
  border:1.5px solid rgba(200,169,106,.3);
  border-radius:7px; padding:.52rem .6rem;
  font-size:.75rem; font-weight:600; color:var(--gold);
  font-family:var(--sans); cursor:pointer;
  transition:all .22s; white-space:nowrap;
}
.btn-card-waitlist:hover {
  background:rgba(200,169,106,.18);
  border-color:var(--gold);
}
.btn-pledge {
  display:inline-flex; align-items:center; justify-content:center; gap:.35rem;
  background:transparent;
  border:1.5px solid var(--border);
  border-radius:7px; padding:.52rem .6rem;
  font-size:.75rem; font-weight:500; color:var(--muted);
  font-family:var(--sans); cursor:pointer;
  transition:all .22s; white-space:nowrap;
}
.btn-pledge:hover { border-color:rgba(200,169,106,.35); color:var(--text); }
.btn-pledge.pledged {
  background:rgba(62,181,117,.08);
  border-color:rgba(62,181,117,.35);
  color:var(--green);
  font-weight:600;
}
.pledge-social {
  font-size:.7rem; color:var(--muted); text-align:center;
  min-height:.9rem; transition:opacity .3s;
}
.pledge-social.has-count { color:var(--gold); }
"""

files['src/components/ProductCard.jsx'] = """import React, { useContext, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { togglePledge as apiTogglePledge } from '../api';
import './ProductCard.css';

function ProductCard({ product, index, onJoinWaitlist }) {
  const { isLoggedIn } = useContext(AuthContext);
  const navigate = useNavigate();
  const location = useLocation();

  const [pledged, setPledged] = useState(product.user_pledged || false);
  const [pledgeCount, setPledgeCount] = useState(product.pledge_count || 0);

  const handleJoin = () => {
    if (!isLoggedIn) {
      navigate('/login', { state: { from: location.pathname } });
    } else {
      onJoinWaitlist(product);
    }
  };

  const handlePledge = async () => {
    if (!isLoggedIn) {
      navigate('/login', { state: { from: location.pathname } });
      return;
    }
    
    // optimistic
    const wasPledged = pledged;
    setPledged(!wasPledged);
    setPledgeCount(c => wasPledged ? c - 1 : c + 1);

    try {
      const res = await apiTogglePledge(product.id);
      setPledged(res.data.pledged);
      setPledgeCount(res.data.pledge_count);
    } catch (e) {
      console.error(e);
      // revert
      setPledged(wasPledged);
      setPledgeCount(c => !wasPledged ? c - 1 : c + 1);
    }
  };

  const savePct = Math.round((1 - product.ah_price / product.market_price) * 100);

  return (
    <div className="product-card reveal" style={{animationDelay: `${index * 0.06}s`}}>
      <div className="product-img">
        <img src={product.image || 'https://via.placeholder.com/600'} alt={product.name} />
        <div className="product-img-overlay" />
        {product.tag && <span className="product-tag">{product.tag}</span>}
      </div>
      <div className="product-body">
        <p className="product-name">{product.name}</p>
        <p className="product-sub">{product.subtitle}</p>
        <div className="product-footer">
          <div className="product-prices">
            <span className="price-ah">Rs. {product.ah_price.toLocaleString('en-IN')}</span>
            <span className="price-mkt">Rs. {product.market_price.toLocaleString('en-IN')}</span>
            <span className="price-save">-{savePct}%</span>
          </div>
          <div className="card-actions">
            <button className="btn-card-waitlist" onClick={handleJoin}>Join Waitlist</button>
            <button className={`btn-pledge ${pledged ? 'pledged' : ''}`} onClick={handlePledge}>
              {pledged ? "✓ I'll order this" : "I'll order this"}
            </button>
          </div>
          <p className={`pledge-social ${pledgeCount > 0 ? 'has-count' : ''}`}>
            {pledgeCount > 0 ? `${pledgeCount} ${pledgeCount === 1 ? 'person' : 'people'} plan to order this` : ''}
          </p>
        </div>
      </div>
    </div>
  );
}

export default ProductCard;
"""

files['src/components/WaitlistModal.css'] = """/* ── MODAL OVERLAY ── */
#modal-overlay {
  display:none; position:fixed; inset:0; z-index:300;
  background:rgba(5,5,5,.88); backdrop-filter:blur(12px);
  align-items:center; justify-content:center;
  padding:1.5rem;
}
#modal-overlay.open { display:flex; }
.modal {
  background:var(--surface);
  border:1px solid rgba(200,169,106,.25);
  border-radius:18px; width:100%; max-width:400px;
  padding:2rem; animation:fadeUp .3s ease; position:relative;
}
.modal-close {
  position:absolute; top:1rem; right:1rem;
  background:none; border:none; color:var(--muted);
  font-size:1.2rem; cursor:pointer; padding:.3rem; transition:color .2s;
}
.modal-close:hover { color:var(--cream); }
.modal-title { font-family:var(--serif); font-size:1.5rem; color:var(--cream); margin-bottom:.4rem; }
.modal-sub { font-size:.84rem; color:var(--muted); margin-bottom:1.2rem; line-height:1.65; }
.modal-form { display:flex; flex-direction:column; gap:.85rem; }
.form-input {
  background:var(--bg); border:1.5px solid var(--border); border-radius:8px; padding:.78rem 1rem;
  color:var(--cream); font-size:.9rem; font-family:var(--sans); outline:none; transition:border-color .2s;
}
.form-input:focus { border-color:var(--gold); }
.form-success {
  background:rgba(62,181,117,.07); border:1px solid rgba(62,181,117,.25); border-radius:10px; padding:1.5rem; text-align:center;
}
"""

files['src/components/WaitlistModal.jsx'] = """import React, { useState } from 'react';
import { joinWaitlist } from '../api';
import './WaitlistModal.css';

function WaitlistModal({ product, onClose }) {
  const [form, setForm] = useState({ name: '', phone: '', city: '', requirements: '' });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);

  if (!product) return null;

  const handleChange = e => setForm({...form, [e.target.name]: e.target.value});

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await joinWaitlist({ ...form, product: product.id });
      setSuccess(true);
    } catch (err) {
      if (err.response?.data?.error) {
         setError(err.response.data.error);
      } else {
         setError("Something went wrong. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div id="modal-overlay" className="open" onClick={(e) => e.target.id === 'modal-overlay' && onClose()}>
      <div className="modal">
        <button className="modal-close" onClick={onClose}>✕</button>
        {success ? (
          <div className="form-success">
            <div style={{fontSize:'2rem', marginBottom:'.6rem'}}>✅</div>
            <p className="modal-title">You're on the list!</p>
            <p className="modal-sub">You have successfully joined the waitlist for {product.name}. We'll reserve your early-bird discount.</p>
            <button className="btn-primary" onClick={onClose} style={{marginTop:'1rem', width:'100%'}}>Close</button>
          </div>
        ) : (
          <>
            <p className="modal-title">Join the Waitlist</p>
            <p className="modal-sub">For: <strong style={{color:'var(--gold)'}}>{product.name} (Rs. {product.ah_price.toLocaleString()})</strong></p>
            
            {error && <div style={{color:'#E57373', fontSize:'.85rem', marginBottom:'1rem'}}>{error}</div>}

            <form className="modal-form" onSubmit={handleSubmit}>
              <div style={{display:'flex', flexDirection:'column', gap:'.4rem'}}>
                <label style={{fontSize:'.7rem', fontWeight:'600', color:'var(--muted)'}}>Full Name</label>
                <input name="name" required className="form-input" value={form.name} onChange={handleChange} />
              </div>
              <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'.8rem'}}>
                <div style={{display:'flex', flexDirection:'column', gap:'.4rem'}}>
                  <label style={{fontSize:'.7rem', fontWeight:'600', color:'var(--muted)'}}>Phone</label>
                  <input name="phone" required className="form-input" value={form.phone} onChange={handleChange} />
                </div>
                <div style={{display:'flex', flexDirection:'column', gap:'.4rem'}}>
                  <label style={{fontSize:'.7rem', fontWeight:'600', color:'var(--muted)'}}>City</label>
                  <input name="city" required className="form-input" value={form.city} onChange={handleChange} />
                </div>
              </div>
              <div style={{display:'flex', flexDirection:'column', gap:'.4rem'}}>
                <label style={{fontSize:'.7rem', fontWeight:'600', color:'var(--muted)'}}>Customisation / Requirements</label>
                <textarea name="requirements" className="form-input" rows="2" value={form.requirements} onChange={handleChange}></textarea>
              </div>
              
              <button type="submit" className="btn-primary" disabled={loading} style={{marginTop:'.5rem'}}>
                {loading ? 'Joining...' : 'Save My Spot'}
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
}

export default WaitlistModal;
"""

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
