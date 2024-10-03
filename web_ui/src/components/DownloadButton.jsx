import React from 'react';

function DownloadButton() {
  const handleDownload = () => {
    window.location.href = '/api/download_code';
  };

  return (
    <button className="download-button" onClick={handleDownload}>
      Download Code
    </button>
  );
}

export default DownloadButton;
