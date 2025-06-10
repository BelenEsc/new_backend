// src/components/RequestForm.js
import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './styles.css';

function RequestForm() {
    const [formData, setFormData] = useState({
        
// Requester Information
        first_name: '',
        last_name: '',
        contact_person_email: '',
        requester_institution: '',
        institution_location: '',
        
// Request
        tissue_sample_quantity: '',
        aliquot_sample_quantity: '',
        manifest_file: null,
       
 // Sample Metadata
        original_sample_id: '',
        taxon_group: '',
        family: '',
        genus: '',
        scientific_name: '',
        interspecific_epithet: '',
        collector_sample_id: '',
        collector: '',
        collector_affiliation: '',
        date_of_collection: '',
        collection_location: '',
        decimal_latitude: '',
        decimal_longitude: '',
        habitat: '',
        elevation: '',
        identified_by: '',
        voucher_id: '',
        voucher_link: '',
        voucher_institution: '',
      
// Permits and Files
        sampling_permits_required: false,
        sampling_permits_file: null,
        nagoya_permits_required: false,
        nagoya_permits_file: null,
        
// Shipping Information
        shipment_date: '',
        tracking_number: ''
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [progress, setProgress] = useState(0);

    const handleChange = (event) => {
        const { name, value, type, checked } = event.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    const handleFileChange = (event) => {
        const { name, files } = event.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: files[0]
        }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        setError(null);
        setProgress(0);

        try {
            // Validaciones
            if (!formData.first_name || !formData.last_name || !formData.contact_person_email) {
                throw new Error('Debes completar los campos requeridos del solicitante');
            }

            // Crear FormData
            const formDataToSend = new FormData();
            Object.entries(formData).forEach(([key, value]) => {
                if (value !== null && !(value instanceof File)) {
                    formDataToSend.append(key, value.toString());
                }
            });

            // Agregar archivos
            if (formData.manifest_file instanceof File) {
                formDataToSend.append('manifest_file', formData.manifest_file);
            }
            if (formData.sampling_permits_file instanceof File) {
                formDataToSend.append('sampling_permits_file', formData.sampling_permits_file);
            }
            if (formData.nagoya_permits_file instanceof File) {
                formDataToSend.append('nagoya_permits_file', formData.nagoya_permits_file);
            }

            // Configuración de Axios con seguimiento de progreso
            const config = {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                onUploadProgress: (progressEvent) => {
                    const percentCompleted = Math.round(
                        (progressEvent.loaded * 100) / progressEvent.total
                    );
                    setProgress(percentCompleted);
                }
            };

            // Enviar la solicitud
            const startTime = Date.now();
            const response = await axios.post('/api/storage-requests/', formDataToSend, config);
            
            console.log(`Tiempo total de envío: ${(Date.now() - startTime) / 1000} segundos`);
            
            if (response.status === 200) {
                console.log('Formulario enviado exitosamente:', response.data);
                setFormData({
                    // ... limpiar el formulario ...
                });
                alert('¡Formulario enviado exitosamente!');
            }
        } catch (error) {
            console.error('Error:', error);
            setError(error.message || 'Error al enviar el formulario');
        } finally {
            setLoading(false);
        }
    };
    return (
        <div className="form-container">
            <div className="logo-section">
                <img
                    src="https://www.bgbm.org/sites/default/files/styles/150px_width/public/images/pr/bo_logo-big-online_rgb-midnightgreen.jpg?itok=MGlNUGNW"
                    alt="BGBM Logo"
                    height="120px"
                />
            </div>
            <div className="header-section">
                <h1>DNA Sample Storage - Request Form</h1>
                <h2>Please fill out one form per requested sample. A sample is defined as any type of material derived from a single specimen.</h2>
            </div>
            <form id="storageRequestForm" onSubmit={handleSubmit}>
                {/* Requester Information Section */}
                <section id="Requester">
                    <h3><strong>Requester Information:</strong></h3>
                    <div className="form-group">
                        <label htmlFor="first_name">First Name:</label>
                        <input
                            type="text"
                            id="first_name"
                            name="first_name"
                            value={formData.first_name}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="last_name">Last Name:</label>
                        <input
                            type="text"
                            id="last_name"
                            name="last_name"
                            value={formData.last_name}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="contact_person_email">Email Address:</label>
                        <input
                            type="email"
                            id="contact_person_email"
                            name="contact_person_email"
                            value={formData.contact_person_email}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="requester_institution">Institution:</label>
                        <input
                            type="text"
                            id="requester_institution"
                            name="requester_institution"
                            value={formData.requester_institution}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="institution_location">Institution Location:</label>
                        <input
                            type="text"
                            id="institution_location"
                            name="institution_location"
                            value={formData.institution_location}
                            onChange={handleChange}
                        />
                    </div>
                </section>

                {/* Request Section */}
                <section id="Request">
                    <h3><strong>Request:</strong></h3>
                    <div className="form-group">
                        <label htmlFor="tissue_sample_quantity">Tissue Sample IDs Quantity Required:</label>
                        <input
                            type="number"
                            id="tissue_sample_quantity"
                            name="tissue_sample_quantity"
                            value={formData.tissue_sample_quantity}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="aliquot_sample_quantity">Aliquot Sample IDs Quantity Required:</label>
                        <input
                            type="number"
                            id="aliquot_sample_quantity"
                            name="aliquot_sample_quantity"
                            value={formData.aliquot_sample_quantity}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="manifest_file">Manifest File:</label>
                        <input
                            type="file"
                            id="manifest_file"
                            name="manifest_file"
                            onChange={handleFileChange}
                        />
                    </div>
                </section>

                {/* Sample Metadata Section */}
                <section id="Metadata">
                    <h3><strong>Sample Metadata:</strong></h3>
                    <div className="form-group">
                        <label htmlFor="original_sample_id">Original Sample ID:</label>
                        <input
                            type="text"
                            id="original_sample_id"
                            name="original_sample_id"
                            value={formData.original_sample_id}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="taxon_group">Taxon Group:</label>
                        <input
                            type="text"
                            id="taxon_group"
                            name="taxon_group"
                            value={formData.taxon_group}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="family">Family:</label>
                        <input
                            type="text"
                            id="family"
                            name="family"
                            value={formData.family}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="genus">Genus:</label>
                        <input
                            type="text"
                            id="genus"
                            name="genus"
                            value={formData.genus}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="scientific_name">Scientific Name:</label>
                        <input
                            type="text"
                            id="scientific_name"
                            name="scientific_name"
                            value={formData.scientific_name}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="interspecific_epithet">Interspecific Epithet:</label>
                        <input
                            type="text"
                            id="interspecific_epithet"
                            name="interspecific_epithet"
                            value={formData.interspecific_epithet}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="collector_sample_id">Collector Sample Number:</label>
                        <input
                            type="text"
                            id="collector_sample_id"
                            name="collector_sample_id"
                            value={formData.collector_sample_id}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="collector">Collector:</label>
                        <input
                            type="text"
                            id="collector"
                            name="collector"
                            value={formData.collector}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="collector_affiliation">Collector Affiliation:</label>
                        <input
                            type="text"
                            id="collector_affiliation"
                            name="collector_affiliation"
                            value={formData.collector_affiliation}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="collection_date">Date of Collection:</label>
                        <input
                            type="date"
                            id="collection_date"
                            name="collection_date"
                            value={formData.collection_date}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="collection_location">Collection Location:</label>
                        <input
                            type="text"
                            id="collection_location"
                            name="collection_location"
                            value={formData.collection_location}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="decimal_latitude">Decimal Latitude:</label>
                        <input
                            type="text"
                            id="decimal_latitude"
                            name="decimal_latitude"
                            value={formData.decimal_latitude}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="decimal_longitude">Decimal Longitude:</label>
                        <input
                            type="text"
                            id="decimal_longitude"
                            name="decimal_longitude"
                            value={formData.decimal_longitude}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="habitat">Habitat:</label>
                        <input
                            type="text"
                            id="habitat"
                            name="habitat"
                            value={formData.habitat}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="elevation">Elevation (m):</label>
                        <input
                            type="number"
                            id="elevation"
                            name="elevation"
                            value={formData.elevation}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="identified_by">Identified By:</label>
                        <input
                            type="text"
                            id="identified_by"
                            name="identified_by"
                            value={formData.identified_by}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="voucher_id">Voucher ID:</label>
                        <input
                            type="text"
                            id="voucher_id"
                            name="voucher_id"
                            value={formData.voucher_id}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="voucher_link">Voucher Link:</label>
                        <input
                            type="url"
                            id="voucher_link"
                            name="voucher_link"
                            value={formData.voucher_link}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="voucher_institution">Voucher Institution:</label>
                        <input
                            type="text"
                            id="voucher_institution"
                            name="voucher_institution"
                            value={formData.voucher_institution}
                            onChange={handleChange}
                        />
                    </div>
                </section>

                {/* Permits and Files Section */}
                <section id="Permits">
                    <h3><strong>Permits and Files:</strong></h3>
                    <div className="form-group">
                        <label htmlFor="sampling_permits_required">Sampling Permits Required:</label>
                        <input
                            type="checkbox"
                            id="sampling_permits_required"
                            name="sampling_permits_required"
                            checked={formData.sampling_permits_required}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="sampling_permits_file">Sampling Permits File:</label>
                        <input
                            type="file"
                            id="sampling_permits_file"
                            name="sampling_permits_file"
                            onChange={handleFileChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="nagoya_permits_required">Nagoya Permits Required:</label>
                        <input
                            type="checkbox"
                            id="nagoya_permits_required"
                            name="nagoya_permits_required"
                            checked={formData.nagoya_permits_required}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="nagoya_permits_file">Nagoya Permits File:</label>
                        <input
                            type="file"
                            id="nagoya_permits_file"
                            name="nagoya_permits_file"
                            onChange={handleFileChange}
                        />
                    </div>
                </section>

                {/* Shipping Information Section */}
                <section id="Shipment">
                    <h3><strong>Shipping Information:</strong></h3>
                    <div className="form-group">
                        <label htmlFor="shipment_date">Shipment Date:</label>
                        <input
                            type="date"
                            id="shipment_date"
                            name="shipment_date"
                            value={formData.shipment_date}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="tracking_number">Tracking Number:</label>
                        <input
                            type="text"
                            id="tracking_number"
                            name="tracking_number"
                            value={formData.tracking_number}
                            onChange={handleChange}
                        />
                    </div>
                </section>

                <div>
                    <button type="submit">Submit Form</button>
                </div>
            </form>
        </div>
    );
}

export default RequestForm;