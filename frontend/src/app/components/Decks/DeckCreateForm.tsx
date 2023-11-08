import React from 'react';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import { useRequiredField, useAppDispatch } from '../../hooks';
import { createDeck } from '../../slices/decksSlice';

import DynamicForm from '../Layout/DynamicForm';

export interface IProps {
  open: boolean
  handleClose: () => void
}

const DeckCreateForm = ({ open, handleClose }: IProps): React.JSX.Element => {
  const name = useRequiredField('Name', 'text');
  const dispatch = useAppDispatch();

  const myHandleClose = (): void => {
    handleClose();
    name.clear();
  };

  const handleSubmit = (): void => {
    if (name.validate()) {
      handleClose();
      void dispatch(createDeck(name.value));
      name.clear();
    }
  };

  return (
    <DynamicForm
      title="Create a deck"
      handleSubmit={handleSubmit}
      handleClose={myHandleClose}
      open={open}
    >
      <Grid container>
        <Grid item xs={12} >
          <TextField
            required
            fullWidth
            label="Name"
            variant="outlined"
            {...name.inputProps}
          />
        </Grid>
      </Grid>
    </DynamicForm>
  );
};

export default DeckCreateForm;
