use Google\Cloud\Firestore\FirestoreClient;

/**
 * Initialize Cloud Firestore with default project ID.
 * ```
 * initialize();
 * ```
 */
function initialize()
{
    // Create the Cloud Firestore client
    $db = new FirestoreClient();
    printf('Created Cloud Firestore client with default project ID.' . PHP_EOL);
}
$docRef = $db->collection('users')->document('lovelace');
$docRef->set([
    'first' => 'Ada',
    'last' => 'Lovelace',
    'born' => 1815
]);
printf('Added data to the lovelace document in the users collection.' . PHP_EOL);
$docRef = $db->collection('users')->document('aturing');
$docRef->set([
    'first' => 'Alan',
    'middle' => 'Mathison',
    'last' => 'Turing',
    'born' => 1912
]);
printf('Added data to the aturing document in the users collection.' . PHP_EOL);

$usersRef = $db->collection('users');
$snapshot = $usersRef->documents();
foreach ($snapshot as $user) {
    printf('User: %s' . PHP_EOL, $user->id());
    printf('First: %s' . PHP_EOL, $user['first']);
    if (!empty($user['middle'])) {
        printf('Middle: %s' . PHP_EOL, $user['middle']);
    }
    printf('Last: %s' . PHP_EOL, $user['last']);
    printf('Born: %d' . PHP_EOL, $user['born']);
    printf(PHP_EOL);
}
printf('Retrieved and printed out all documents from the users collection.' . PHP_EOL);
