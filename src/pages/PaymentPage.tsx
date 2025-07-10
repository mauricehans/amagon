import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { CreditCard, Lock, Download, CheckCircle } from 'lucide-react';
import jsPDF from "jspdf";

interface PaymentFormData {
  cardNumber: string;
  cardHolder: string;
  expiryMonth: string;
  expiryYear: string;
  cvv: string;
  billingAddress: {
    street: string;
    city: string;
    state: string;
    zip: string;
    country: string;
  };
}

interface Product {
  id: string;
  name: string;
  price: number;
  image_url: string;
  quantity: number;
}

const PaymentPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [isProcessing, setIsProcessing] = useState(false);
  const [paymentSuccess, setPaymentSuccess] = useState(false);
  const [receiptUrl, setReceiptUrl] = useState<string | null>(null);
  
  // Récupérer les données des produits depuis la navigation (panier ou achat direct)
  const products: Product[] = location.state?.products || (location.state?.product ? [location.state.product] : []);

  const [formData, setFormData] = useState<PaymentFormData>({
    cardNumber: '',
    cardHolder: '',
    expiryMonth: '',
    expiryYear: '',
    cvv: '',
    billingAddress: {
      street: '',
      city: '',
      state: '',
      zip: '',
      country: 'France'
    }
  });

  const handleInputChange = (field: string, value: string) => {
    if (field.includes('.')) {
      const [parent, child] = field.split('.');
      setFormData(prev => ({
        ...prev,
        [parent]: {
          ...prev[parent as keyof PaymentFormData],
          [child]: value
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [field]: value
      }));
    }
  };

  const formatCardNumber = (value: string) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    const matches = v.match(/\d{4,16}/g);
    const match = matches && matches[0] || '';
    const parts = [];
    for (let i = 0, len = match.length; i < len; i += 4) {
      parts.push(match.substring(i, i + 4));
    }
    if (parts.length) {
      return parts.join(' ');
    } else {
      return v;
    }
  };

  const handleCardNumberChange = (value: string) => {
    const formatted = formatCardNumber(value);
    handleInputChange('cardNumber', formatted);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsProcessing(true);
    
    // Simuler le traitement du paiement
    setTimeout(() => {
      setIsProcessing(false);
      setPaymentSuccess(true);
      
      // Simuler la génération du reçu PDF
      setTimeout(() => {
        setReceiptUrl('/receipt.pdf'); // URL fictive du PDF
      }, 1000);
    }, 2000);
  };

  const downloadReceipt = () => {
    const doc = new jsPDF();
    doc.setFontSize(16);
    doc.text("Reçu de paiement", 10, 15);

    doc.setFontSize(12);
    let y = 30;
    doc.text("Produits achetés :", 10, y);
    y += 8;

    products.forEach((p, idx) => {
      doc.text(
        `${idx + 1}. ${p.name} — ${Number(p.price).toFixed(2)} € x ${p.quantity || 1}`,
        10,
        y
      );
      y += 8;
    });

    y += 4;
    doc.text(`Total : ${total.toFixed(2)} €`, 10, y);

    y += 10;
    doc.text("Merci pour votre achat !", 10, y);

    doc.save("recu-commande.pdf");
  };

  if (!products || products.length === 0) {
    return (
      <div className="container-custom py-8 text-center">
        <h1 className="text-2xl font-bold mb-4">Erreur</h1>
        <p className="mb-6">Aucun produit sélectionné pour l'achat.</p>
        <button 
          onClick={() => navigate('/')}
          className="btn btn-primary"
        >
          Retour à l'accueil
        </button>
      </div>
    );
  }

  const total = products.reduce((sum, p) => sum + p.price * (p.quantity || 1), 0);

  if (paymentSuccess) {
    return (
      <div className="container-custom py-8">
        <div className="max-w-md mx-auto text-center">
          <CheckCircle size={64} className="text-amazon-success mx-auto mb-4" />
          <h1 className="text-2xl font-bold mb-4">Paiement réussi !</h1>
          <p className="mb-6">Votre commande a été traitée avec succès.</p>
          <div className="mb-6 text-left">
            <h3 className="font-bold mb-2">Produits achetés :</h3>
            <ul>
              {products.map((p) => (
                <li key={p.id} className="mb-2">
                  <span className="font-medium">{p.name}</span> — {Number(p.price).toFixed(2)} € x {p.quantity || 1}
                </li>
              ))}
            </ul>
            <div className="font-bold mt-2">Total : {total.toFixed(2)} €</div>
          </div>
          {receiptUrl && (
            <button 
              onClick={downloadReceipt}
              className="btn btn-primary flex items-center justify-center mx-auto"
            >
              <Download size={20} className="mr-2" />
              Télécharger le reçu PDF
            </button>
          )}
          <button 
            onClick={() => navigate('/')}
            className="btn btn-outline mt-4"
          >
            Retour à l'accueil
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gray-100 min-h-screen">
      <div className="container-custom py-8">
        <h1 className="text-2xl font-bold mb-6">Informations de paiement</h1>
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Formulaire de paiement */}
          <div className="lg:w-2/3">
            <div className="bg-white p-6 rounded shadow-sm">
              <div className="flex items-center mb-4">
                <Lock size={20} className="text-amazon-teal mr-2" />
                <span className="text-sm text-gray-600">Vos informations de paiement sont sécurisées</span>
              </div>
              <form onSubmit={handleSubmit}>
                <div className="mb-6">
                  <h3 className="font-bold text-lg mb-4">Carte de crédit ou de débit</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="md:col-span-2">
                      <label className="form-label">Numéro de carte</label>
                      <input 
                        type="text"
                        value={formData.cardNumber}
                        onChange={(e) => handleCardNumberChange(e.target.value)}
                        placeholder="1234 5678 9012 3456"
                        className="form-input"
                        maxLength={19}
                        required
                      />
                    </div>
                    <div className="md:col-span-2">
                      <label className="form-label">Nom du titulaire</label>
                      <input 
                        type="text"
                        value={formData.cardHolder}
                        onChange={(e) => handleInputChange('cardHolder', e.target.value)}
                        className="form-input"
                        required
                      />
                    </div>
                    <div>
                      <label className="form-label">Mois d'expiration</label>
                      <select 
                        value={formData.expiryMonth}
                        onChange={(e) => handleInputChange('expiryMonth', e.target.value)}
                        className="form-input"
                        required
                      >
                        <option value="">Mois</option>
                        {Array.from({ length: 12 }, (_, i) => i + 1).map(month => (
                          <option key={month} value={month.toString().padStart(2, '0')}>
                            {month.toString().padStart(2, '0')}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="form-label">Année d'expiration</label>
                      <select 
                        value={formData.expiryYear}
                        onChange={(e) => handleInputChange('expiryYear', e.target.value)}
                        className="form-input"
                        required
                      >
                        <option value="">Année</option>
                        {Array.from({ length: 10 }, (_, i) => new Date().getFullYear() + i).map(year => (
                          <option key={year} value={year}>{year}</option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="form-label">Code de sécurité (CVV)</label>
                      <input 
                        type="text"
                        value={formData.cvv}
                        onChange={(e) => handleInputChange('cvv', e.target.value)}
                        placeholder="123"
                        className="form-input"
                        maxLength={4}
                        required
                      />
                    </div>
                  </div>
                </div>
                <div className="mb-6">
                  <h3 className="font-bold text-lg mb-4">Adresse de facturation</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="md:col-span-2">
                      <label className="form-label">Adresse</label>
                      <input 
                        type="text"
                        value={formData.billingAddress.street}
                        onChange={(e) => handleInputChange('billingAddress.street', e.target.value)}
                        className="form-input"
                        required
                      />
                    </div>
                    <div>
                      <label className="form-label">Ville</label>
                      <input 
                        type="text"
                        value={formData.billingAddress.city}
                        onChange={(e) => handleInputChange('billingAddress.city', e.target.value)}
                        className="form-input"
                        required
                      />
                    </div>
                    <div>
                      <label className="form-label">État/Région</label>
                      <input 
                        type="text"
                        value={formData.billingAddress.state}
                        onChange={(e) => handleInputChange('billingAddress.state', e.target.value)}
                        className="form-input"
                        required
                      />
                    </div>
                    <div>
                      <label className="form-label">Code postal</label>
                      <input 
                        type="text"
                        value={formData.billingAddress.zip}
                        onChange={(e) => handleInputChange('billingAddress.zip', e.target.value)}
                        className="form-input"
                        required
                      />
                    </div>
                    <div>
                      <label className="form-label">Pays</label>
                      <select 
                        value={formData.billingAddress.country}
                        onChange={(e) => handleInputChange('billingAddress.country', e.target.value)}
                        className="form-input"
                        required
                      >
                        <option value="France">France</option>
                        <option value="Germany">Allemagne</option>
                        <option value="United Kingdom">Royaume-Uni</option>
                        <option value="Italy">Italie</option>
                        <option value="Spain">Espagne</option>
                      </select>
                    </div>
                  </div>
                </div>
                <button 
                  type="submit"
                  disabled={isProcessing}
                  className="btn btn-primary w-full"
                >
                  {isProcessing ? 'Traitement en cours...' : `Payer ${total.toFixed(2)} €`}
                </button>
              </form>
            </div>
          </div>
          {/* Résumé de la commande */}
          <div className="lg:w-1/3">
            <div className="bg-white p-6 rounded shadow-sm sticky top-4">
              <h3 className="font-bold text-lg mb-4">Résumé de la commande</h3>
              {products.map((p) => (
                <div key={p.id} className="flex items-center mb-4">
                  <img 
                    src={p.image_url} 
                    alt={p.name}
                    className="w-16 h-16 object-contain mr-4"
                  />
                  <div>
                    <h4 className="font-medium">{p.name}</h4>
                    <p className="text-sm text-gray-600">Quantité: {p.quantity || 1}</p>
                    <p className="text-sm text-gray-600">Prix unitaire: {Number(p.price).toFixed(2)} €</p>
                  </div>
                </div>
              ))}
              <div className="border-t border-gray-200 pt-4">
                <div className="flex justify-between mb-2">
                  <span>Sous-total:</span>
                  <span>{total.toFixed(2)} €</span>
                </div>
                <div className="flex justify-between mb-2">
                  <span>Livraison:</span>
                  <span>Gratuit</span>
                </div>
                <div className="flex justify-between mb-2">
                  <span>TVA:</span>
                  <span>{(total * 0.20).toFixed(2)} €</span>
                </div>
                <div className="flex justify-between font-bold text-lg border-t border-gray-200 pt-2">
                  <span>Total:</span>
                  <span>{(total * 1.20).toFixed(2)} €</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PaymentPage; 