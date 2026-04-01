import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getMyWaitlist } from '../api';
import './Home.css'; // Reuse container styles

function MyWaitlist() {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMyWaitlist().then(res => {
      setEntries(res.data);
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, []);

  return (
    <div style={{paddingTop: '6rem', minHeight: '100vh'}}>
      <section>
        <h2 className="section-title">My Waitlist Entries</h2>
        
        {loading ? (
          <p className="section-sub">Loading your entries...</p>
        ) : entries.length === 0 ? (
          <div style={{marginTop: '2rem'}}>
            <p className="section-sub" style={{marginBottom: '1.5rem'}}>You haven't joined any waitlists yet.</p>
            <Link to="/" className="btn-primary">Browse Products</Link>
          </div>
        ) : (
          <div className="products-grid" style={{marginTop: '2rem'}}>
            {entries.map(entry => (
              <div key={entry.id} className="product-card" style={{border: '1px solid rgba(62,181,117,.3)'}}>
                <div className="product-img">
                  <img src={entry.product.image} alt={entry.product.name} />
                  <span className="product-tag" style={{background:'rgba(62,181,117,.15)', color:'var(--green)', borderColor:'var(--green)'}}>Waitlisted</span>
                </div>
                <div className="product-body">
                  <p className="product-name">{entry.product.name}</p>
                  <p className="product-sub" style={{textTransform:'uppercase', fontSize:'.7rem'}}>{entry.product.category}</p>
                  <div className="product-prices">
                    <span className="price-ah">Rs. {entry.product.ah_price?.toLocaleString()}</span>
                  </div>
                  {entry.requirements && (
                    <div style={{marginTop:'.8rem', fontSize:'.8rem', color:'var(--text)', background:'var(--bg)', padding:'.5rem', borderRadius:'6px'}}>
                      <strong>Req:</strong> {entry.requirements}
                    </div>
                  )}
                  <p style={{fontSize:'.75rem', color:'var(--muted)', marginTop:'.8rem'}}>Joined on {new Date(entry.created_at).toLocaleDateString()}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

export default MyWaitlist;
