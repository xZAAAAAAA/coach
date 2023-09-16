import 'package:oauth2_client/oauth2_client.dart';

class WhoopClient extends OAuth2Client {
  WhoopClient({required String customUriScheme})
      : super(
            credentialsLocation: CredentialsLocation.body,
            authorizeUrl: 'https://api.prod.whoop.com/oauth/oauth2/auth',
            tokenUrl: 'https://api.prod.whoop.com/oauth/oauth2/token',
            redirectUri: 'com.coach.coach://whoop',
            customUriScheme: 'com.coach.coach');
}
