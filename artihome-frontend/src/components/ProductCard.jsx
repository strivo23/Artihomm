import React, { useContext, useState } from 'react';
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

  // Backend compat: Map estimated_price to ah_price, simulate market_price if missing
  const ahPrice = product.ah_price !== undefined ? parseFloat(product.ah_price) : parseFloat(product.estimated_price) || 0;
  const marketPrice = product.market_price !== undefined ? parseFloat(product.market_price) : ahPrice * 1.8;
  const savePct = Math.round((1 - (ahPrice / marketPrice)) * 100);

  return (
    <div className="product-card reveal" style={{ transitionDelay: `${(index % 3) * 0.1}s` }}>
      <div className="product-img-box">
        <img src={product.image || product.image_url || 'https://via.placeholder.com/600'} alt={product.name} />
        <div className="product-img-overlay" />
        {product.tag && <span className="product-tag">{product.tag}</span>}
      </div>
      <div className="product-body">
        <p className="product-name">{product.name}</p>
        <p className="product-sub">{product.subtitle || product.description?.substring(0, 50)}</p>
        <div className="product-footer">
          <div className="product-prices">
            <span className="price-ah">Rs. {ahPrice.toLocaleString('en-IN')}</span>
            <span className="price-mkt">Rs. {marketPrice.toLocaleString('en-IN')}</span>
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
