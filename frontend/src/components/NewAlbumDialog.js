import React from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import { create_or_update_album } from './../server'
import { Redirect } from "react-router-dom";

function NewAlbumDialog(props) {
  const [albumName, setAlbumName] = React.useState("");
  const [description, setDescription] = React.useState("");
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
    <div>
      <Dialog open={props.open} onClose={props.handleClose}>
        <DialogTitle>Create new album</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Every image stored in CameraHub must be connected to an album. Please enter a name and description for your new album below.
          </DialogContentText>
          <TextField
            value={albumName}
            onChange={e => setAlbumName(e.target.value)}
            autoFocus
            margin="dense"
            label="Album name"
            fullWidth
          />
          <TextField
            value={description}
            onChange={e => setDescription(e.target.value)}
            label="Description"
            multiline
            rows={4}
            fullWidth
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={props.handleClose} color="primary">
            Cancel
          </Button>
          <Button onClick={handleSubmit} color="primary">
            Create album
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default NewAlbumDialog
