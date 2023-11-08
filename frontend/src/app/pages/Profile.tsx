import React from 'react';

import {
  Stack,
  TextField,
  Typography
} from '@mui/material';

import Layout from '../components/Layout/Layout';
import { useAppSelector, useRequiredField } from '../hooks';
import Loading from './Loading';
import AvatarEdit from '../components/Layout/AvatarEdit';

const Profile = (): React.JSX.Element => {
  const user = useAppSelector(store => store.user);
  const password = useRequiredField('Password', 'password');

  if (user.entity === null) {
    return <Loading />;
  }

  const handleEditAvatar = (): void => {
    console.log('edit');
  };

  return (
    <Layout>
      <Stack
        direction="row"
        alignItems="center"
        gap={4}
        mb={4}
      >
        <AvatarEdit
          size={68}
          onClick={handleEditAvatar}
        />
        <Typography
          fontSize={34}
        >
          {user.entity.username}
        </Typography>
      </Stack>
      <Typography
        variant="h6"
      >
        Change password
      </Typography>
      <TextField
        required
        fullWidth
        label="Current password"
        variant="standard"
        {...password.inputProps}
      />
      <TextField
        required
        fullWidth
        label="New password"
        variant="standard"
        {...password.inputProps}
      />
      <TextField
        required
        fullWidth
        label="Confirm"
        variant="standard"
        {...password.inputProps}
      />
    </Layout>
  );
};

export default Profile;
