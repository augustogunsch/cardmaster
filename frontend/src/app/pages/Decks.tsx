import React, { useState, useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../hooks';
import { loadDecks } from '../slices/decksSlice';

import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Layout from '../components/Layout/Layout';
import Deck from '../components/Decks/Deck';
import DeckCreateForm from '../components/Decks/DeckCreateForm';
import Paginated from '../components/Layout/Paginated';

const Decks = (): React.JSX.Element => {
  const [open, setOpen] = useState(false);
  const decks = useAppSelector(store => store.decks);
  const dispatch = useAppDispatch();

  useEffect(() => {
    void dispatch(loadDecks());
  }, []);

  return (
    <Layout>
      <Box>
        <Typography
          variant="h4"
          mb={2}
        >
          My decks
        </Typography>
        <Button
          variant="contained"
          color="secondary"
          onClick={() => { setOpen(true); }}
        >
          Create Deck
        </Button>
        <Paginated
          elementNamePlural="decks"
          pageLength={10}
          getElements={decks}
          filter={(deck, filter) => deck.name.toLowerCase().includes(filter)}
          elementMapper={deck => (
            <Deck deck={deck} key={deck.id} />
          )}
        />
      </Box>
      <DeckCreateForm open={open} handleClose={() => { setOpen(false); }}/>
    </Layout>
  );
};

export default Decks;
