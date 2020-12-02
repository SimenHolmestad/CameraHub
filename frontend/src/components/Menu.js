import React, { useState, useEffect } from 'react';
import { get_available_albums } from './../server'
import './NewAlbumForm'
import NewAlbumForm from './NewAlbumForm';
import { Link } from 'react-router-dom';

const useAlbums = () => {
  const [albums, setAlbums] = useState(null);
  useEffect(() => {
    get_available_albums().then((data) => setAlbums(data));
  }, []);
  return albums;
};

function Menu() {
  const albums = useAlbums();

  if (!albums) {
    return <p>loading albums...</p>;
  }

  return (
    <div>
      <p>
        The albums are:
      </p>
      <ul>
        {albums.map(albumName => <li key={albumName}><Link to={ "/album/" + albumName}>{albumName}</Link></li>)}
      </ul>
      <NewAlbumForm/>
    </div>
  );
}

export default Menu;
