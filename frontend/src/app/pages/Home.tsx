import React from 'react';
import { useNavigate } from 'react-router-dom';
import type { NavigateFunction } from 'react-router-dom';

import {
  Box,
  Link,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Typography
} from '@mui/material';
import {
  CloudDownload,
  EditNote,
  MoneyOff,
  Psychology,
  Share
} from '@mui/icons-material';

import Layout from '../components/Layout/Layout';
import Deck from '../components/Home/Deck';
import Paginated from '../components/Layout/Paginated';
import decksService from '../services/deckService';
import type { IDeck } from '../services/deckService';
import { useAppSelector } from '../hooks';
import type { IUserState } from '../slices/userSlice';

const welcomeText = (user: IUserState | null, navigate: NavigateFunction): JSX.Element => {
  if (user === null) {
    return (
      <>
        Welcome to CardMaster. <Link
          sx={{
            '&:hover': {
              cursor: 'pointer'
            }
          }}
          onClick={() => { navigate('/login'); }}
        >
          Create an account or login
        </Link> to start learning
      </>
    );
  } else {
    return (
      <>
        Welcome to CardMaster, {user.username}
      </>
    );
  }
};

const Home = (): React.JSX.Element => {
  const user = useAppSelector(store => store.user);
  const navigate = useNavigate();

  const getDecks = async (
    page: number,
    pageLength: number,
    filter: string
  ): Promise<{
    elements: IDeck[]
    count: number
  }> => {
    const response = await decksService.getDecks({
      q: filter,
      limit: pageLength,
      offset: (page - 1) * pageLength,
      total_count: true,
      card_count: 'all'
    });

    return {
      elements: response.data,
      count: response.count ?? 0
    };
  };

  return (
    <Layout>
      <Box>
        <Typography
          variant="h4"
          mb={4}
        >
          CardMaster
        </Typography>
        <Typography
          mb={2}
        >
          {welcomeText(user.entity, navigate)}. With the power of spaced repetition,
          you will learn what you need to. Explore the platform&apos;s features:
        </Typography>
        <List
          sx={{
            marginBottom: 2
          }}
        >
          <ListItem>
            <ListItemIcon>
              <EditNote />
            </ListItemIcon>
            <ListItemText>
             Create your decks and flash cards.
            </ListItemText>
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <Psychology />
            </ListItemIcon>
            <ListItemText>
             Review and learn new cards daily.
            </ListItemText>
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <Share />
            </ListItemIcon>
            <ListItemText>
             Share your decks with the community.
            </ListItemText>
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <CloudDownload />
            </ListItemIcon>
            <ListItemText>
             Obtain decks from other users.
            </ListItemText>
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <MoneyOff />
            </ListItemIcon>
            <ListItemText>
             Enjoy an ad-free, no subscription experience.
            </ListItemText>
          </ListItem>
        </List>
        <Typography
          mb={4}
        >
          All in a simple, intuitive and open source platform!
        </Typography>
        <Typography
          variant="h6"
          mb={2}
        >
          Community decks
        </Typography>
        <Paginated
          pageLength={10}
          elementNamePlural="decks"
          filter
          elementMapper={deck => (
            <Deck deck={deck} key={deck.id} />
          )}
          getElements={getDecks}
        />
      </Box>
    </Layout>
  );
};

export default Home;
