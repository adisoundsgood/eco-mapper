import React, { useState } from 'react';
import axios from 'axios';
import { UploadCloud, Map } from 'lucide-react';
import Alert from './Alert';

const EcoMapper = () => {
  const [file, setFile] = useState(null);
  const [processType, setProcessType] = useState('ndvi');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setError(null);
  };

  const handleProcessTypeChange = (event) => {
    setProcessType(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      setError('Please select a file to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('process_type', processType);

    setIsLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/api/process', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data.result_url || response.data.result_urls);
      setError(null);
    } catch (err) {
      setError('An error occurred while processing the file.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-xl">
      <h1 className="text-2xl font-bold mb-4">EcoMapper</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex items-center justify-center w-full">
          <label htmlFor="dropzone-file" className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
            <div className="flex flex-col items-center justify-center pt-5 pb-6">
              <UploadCloud className="w-10 h-10 mb-3 text-gray-400" />
              <p className="mb-2 text-sm text-gray-500"><span className="font-semibold">Click to upload</span> or drag and drop</p>
              <p className="text-xs text-gray-500">GeoTIFF file (MAX. 800x400px)</p>
            </div>
            <input id="dropzone-file" type="file" className="hidden" onChange={handleFileChange} accept=".tif,.tiff" />
          </label>
        </div>
        <div>
          <label htmlFor="process-type" className="block text-sm font-medium text-gray-700">
            Processing Type
          </label>
          <select
            id="process-type"
            value={processType}
            onChange={handleProcessTypeChange}
            className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
          >
            <option value="ndvi">NDVI</option>
            <option value="slope_aspect">Slope and Aspect</option>
            <option value="carbon">Carbon Storage</option>
          </select>
        </div>
        <button type="submit" className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" disabled={isLoading}>
          {isLoading ? 'Processing...' : 'Process File'}
        </button>
      </form>
      {error && (
        <Alert variant="destructive" title="Error">
          {error}
        </Alert>
      )}
      {result && (
        <div className="mt-4">
          <h2 className="text-xl font-semibold mb-2">Result</h2>
          {Array.isArray(result) ? (
            result.map((url, index) => (
              <div key={index} className="border border-gray-300 rounded-lg p-4 flex items-center justify-center mb-2">
                <Map className="w-6 h-6 mr-2" />
                <a href={`https://eco-mapper-e076ecd49dfb.herokuapp.com/${url}`} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
                  View Processed Map {index + 1}
                </a>
              </div>
            ))
          ) : (
            <div className="border border-gray-300 rounded-lg p-4 flex items-center justify-center">
              <Map className="w-6 h-6 mr-2" />
              <a href={`https://eco-mapper-e076ecd49dfb.herokuapp.com/${result}`} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
                View Processed Map
              </a>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default EcoMapper;