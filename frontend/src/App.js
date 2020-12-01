import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [albums, setAlbums] = useState([]);

  useEffect(() => {
    fetch('/albums/').then(res => res.json()).then(data => {
      setAlbums(data.available_albums);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <p>
          The albums are:
        </p>
        <ul>
          {albums.map(albumName => <li key={albumName}>{albumName}</li>)}
        </ul>
      </header>
    </div>
  );
}

export default App;
