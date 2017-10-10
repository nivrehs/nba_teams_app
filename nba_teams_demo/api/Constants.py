class Constants:
    # Team Responses
    CREATE_TEAM_SUCCESS = {'http_code': 201,
                           'response': {'status': 'Success',
                                        'description': 'Successfully created team'}}
    CREATE_TEAM_FAILED = {'http_code': 400,
                          'response': {'status': 'Failed',
                                       'description': 'Team was not created due to an error'}}
    UPDATE_TEAM_SUCCESS = {'http_code': 204,
                           'response': {'status': 'Success',
                                        'description': 'Successfully updated team'}}
    UPDATE_TEAM_FAILED = {'http_code': 400,
                          'response': {'status': 'Failed',
                                       'description': 'Team was not updated due to an error'}}
    DELETE_TEAM_FAILED = {'http_code': 400,
                          'response': {'status': 'Failed',
                                       'description': 'Team was not deleted due to an error'}}
    DELETE_TEAM_SUCCESS = {'http_code': 204,
                           'response': {'status': 'Success',
                                        'description': 'Successfully deleted team'}}


    # Team Error Responses
    INVALID_TEAM_ID = {'http_code': 400,
                       'response': {'status': 'Failed',
                                    'description': 'Invalid Team id'}}
    DUPLICATE_TEAM_NAME = {'http_code': 409,
                           'response': {'status': 'Failed',
                                        'description': 'Team name already in the database'}}
    MISSING_TEAM_NAME = {'http_code': 400,
                         'response': {'status': 'Failed',
                                      'description': 'Team name not supplied'}}
    TEAM_NAME_NOT_PROVIDED = {'http_code': 400,
                              'response': {'status': 'Failed',
                                           'description': 'Team name not provided'}}
    TEAM_NOT_FOUND = {'http_code': 404,
                      'response': {'status': 'Failed',
                                   'description': 'Team not found'}}

    # Player Responses
    CREATE_PLAYER_SUCCESS = {'http_code': 201,
                             'response': {'status': 'Success',
                                          'description': 'Successfully created player'}}
    CREATE_PLAYER_FAILED = {'http_code': 400,
                            'response': {'status': 'Failed',
                                         'description': 'Player was not created due to an error'}}
    UPDATE_PLAYER_SUCCESS = {'http_code': 204,
                             'response': {'status': 'Success',
                                          'description': 'Success updated player'}}
    UPDATE_PLAYER_FAILED = {'http_code': 400,
                            'response': {'status': 'Failed',
                                         'description': 'Player was not updated due to an error'}}
    DELETE_PLAYER_FAILED = {'http_code': 400,
                            'response': {'status': 'Failed',
                                         'description': 'Player was not deleted due to an error'}}
    DELETE_PLAYER_SUCCESS = {'http_code': 204,
                             'response': {'status': 'Success',
                                          'description': 'Successfully deleted player'}}
    # Player Error Responses
    MISSING_TEAM_ID = {'http_code': 400,
                       'response': {'status': 'Failed',
                                    'description': 'Team id not provided'}}
    MISSING_PLAYER_NAME = {'http_code': 400,
                           'response': {'status': 'Failed',
                                        'description': 'Player name not provided'}}
    INVALID_PLAYER_ID = {'http_code': 400,
                         'response': {'status': 'Failed',
                                      'description': 'Invalid Player id'}}
    NOTHING_TO_UPDATE = {'http_code': 400,
                         'response': {'status': 'Failed',
                                      'description': 'Nothing to update'}}
    DUPLICATE_PLAYER_NAME = {'http_code': 409,
                             'response': {'status': 'Failed',
                                          'description': 'Player already in the database'}}
    PLAYER_NOT_FOUND = {'http_code': 404,
                        'response': {'status': 'Failed',
                                     'description': 'Player not found'}}

    FREE_AGENTS = 'Free Agents'
