/**
 * A class representing the currently logged-in user.
 */
export class UserToken {
    private readonly _userID: string;
    private readonly _userName: string;

    public constructor(userID: string, userName?: string) {
        this._userID = userID;
        this._userName = userName || userID;
    }

    /**
     * The user ID.
     */
    public get userID(): string {
        return this._userID;
    }

    /**
     * The username.
     */
    public get userName(): string {
        return this._userName;
    }
}
