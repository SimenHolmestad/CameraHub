import React from 'react';
import { create_or_update_album } from './../server'
import { Redirect } from "react-router-dom";

function NewAlbumForm(props) {
  const [albumName, setAlbumName] = React.useState("new_album");
  const [description, setDescription] = React.useState("description");
  const [redirectAlbum, setRedirectAlbum] = React.useState(null);

  const handleSubmit = async (e) => {
  e.preventDefault();
    const response = await create_or_update_album(albumName, description)
    setRedirectAlbum(response.album_name)
  };

  if (redirectAlbum) {
    return <Redirect to={"/album/" + redirectAlbum}/>
  }

  return (
    <form className="input-form" onSubmit={handleSubmit}>
      <input type="text" value={albumName} onChange={e => setAlbumName(e.target.value)} />
      <textarea value={description} onChange={e => setDescription(e.target.value)} />
      <input type="submit" value="Submit" />
    </form>
  );
}

export default NewAlbumForm
