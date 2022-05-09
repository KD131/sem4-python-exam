from flask import Flask,request, abort



@app.route('/push-handlers/receive_messages', methods=['POST'])
def receive_messages_handler():
    # Verify that the request originates from the application.
    if (request.args.get('token', '') !=
            current_app.config['PUBSUB_VERIFICATION_TOKEN']):
        return 'Invalid request', 400

    # Verify that the push request originates from Cloud Pub/Sub.
    try:
        # Get the Cloud Pub/Sub-generated JWT in the "Authorization" header.
        bearer_token = request.headers.get('Authorization')
        token = bearer_token.split(' ')[1]
        TOKENS.append(token)

        # Verify and decode the JWT. `verify_oauth2_token` verifies
        # the JWT signature, the `aud` claim, and the `exp` claim.
        # Note: For high volume push requests, it would save some network
        # overhead if you verify the tokens offline by downloading Google's
        # Public Cert and decode them using the `google.auth.jwt` module;
        # caching already seen tokens works best when a large volume of
        # messages have prompted a single push server to handle them, in which
        # case they would all share the same token for a limited time window.
        claim = id_token.verify_oauth2_token(token, requests.Request(),
                                             audience='example.com')

        # IMPORTANT: you should validate claim details not covered by signature
        # and audience verification above, including:
        #   - Ensure that `claim["email"]` is equal to the expected service
        #     account set up in the push subscription settings.
        #   - Ensure that `claim["email_verified"]` is set to true.

        CLAIMS.append(claim)
    except Exception as e:
        return 'Invalid token: {}\n'.format(e), 400

    envelope = json.loads(request.data.decode('utf-8'))
    payload = base64.b64decode(envelope['message']['data'])
    MESSAGES.append(payload)
    # Returning any 2xx status indicates successful receipt of the message.
    return 'OK', 200