import React, { useState } from 'react';
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
              <p className="modal-sub">For: <strong style={{color:'var(--gold)'}}>{product.name} (Rs. {((product.ah_price !== undefined ? parseFloat(product.ah_price) : parseFloat(product.estimated_price)) || 0).toLocaleString()})</strong></p>
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
