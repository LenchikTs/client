"""DBF record definition.

"""
"""History (most recent first):
30-oct-2006 [als]   fix record length in .fromStream()
04-jul-2006 [als]   added export declaration
20-dec-2005 [yc]    DbfRecord.write() -> DbfRecord._write();
                    added delete() method.
16-dec-2005 [yc]    record definition moved from `dbf`.
"""

__version__ = "$Revision: 1.5 $"[11:-2]
__date__ = "$Date: 2006/10/30 03:06:17 $"[7:-2]

__all__ = ["DbfRecord"]

from itertools import izip

class DbfRecord(object):
    """DBF record.

    Instances of this class shouldn't be created manualy,
    use `dbf.Dbf.newRecord` instead.

    Class implements mapping/sequence interface, so
    fields could be accessed via their names or indexes
    (names is a preferred way to access fields).

    Hint:
        Use `store` method to save modified record.

    Examples:
        Add new record to the database:
            db = Dbf(filename)
            rec = db.newRecord()
            rec["FIELD1"] = value1
            rec["FIELD2"] = value2
            rec.store()
        Or the same, but modify existed
        (second in this case) record:
            db = Dbf(filename)
            rec = db[2]
            rec["FIELD1"] = value1
            rec["FIELD2"] = value2
            rec.store()

    """

    __slots__ = "dbf", "index", "deleted", "fieldData"

    ## creation and initialization

    def __init__(self, dbf, index=None, deleted=False, data=None):
        """Instance initialiation.

        Arguments:
            dbf:
                A `Dbf.Dbf` instance this record belonogs to.
            index:
                An integer record index or None. If this value is
                None, record will be appended to the DBF.
            deleted:
                Boolean flag indicating whether this record
                is a deleted record.
            data:
                A sequence or None. This is a data of the fields.
                If this argument is None, default values will be used.

        """
        self.dbf = dbf
        # XXX: I'm not sure ``index`` is necessary
        self.index = index
        self.deleted = deleted
        if data is None:
            self.fieldData = [_fd.defaultValue for _fd in dbf.header.fields]
        else:
            self.fieldData = list(data)

    # XXX: validate self.index before calculating position?
    position = property(lambda self: self.dbf.header.headerLength + \
        self.index * self.dbf.header.recordLength)

    def fromStream(cls, dbf, index):
        """Return a record read from the stream.

        Arguments:
            dbf:
                A `Dbf.Dbf` instance new record should belong to.
            index:
                Index of the record in the records' container.
                This argument can't be None in this call.

        Return value is an instance of the current class.

        """
        # XXX: may be write smth assuming, that current stream
        # position is the required one? it could save some
        # time required to calculate where to seek in the file
        dbf.stream.seek(dbf.header.headerLength +
            index * dbf.header.recordLength)
        return cls.fromString(dbf,
            dbf.stream.read(dbf.header.recordLength), index)
    fromStream = classmethod(fromStream)

    def fromString(cls, dbf, string, index=None):
        """Return record read from the string object.

        Arguments:
            dbf:
                A `Dbf.Dbf` instance new record should belong to.
            string:
                A string new record should be created from.
            index:
                Index of the record in the container. If this
                argument is None, record will be appended.

        Return value is an instance of the current class.

        """
        return cls(dbf, index, string[0]=="*",
            [_fd.decodeFromRecord(string, dbf) for _fd in dbf.header.fields])
    fromString = classmethod(fromString)

    ## object representation

    def __repr__(self):
        _template = "%%%ds: %%s (%%s)" % max([len(_fld)
            for _fld in self.dbf.fieldNames])
        _rv = []
        for _fld in self.dbf.fieldNames:
            _rv.append(_template % (_fld, self[_fld], type(self[_fld])))
        return "\n".join(_rv)

    ## protected methods

    def _write(self):
        """Write data to the dbf stream.

        Note:
            This isn't a public method, it's better to
            use 'store' instead publically.
            Be design ``_write`` method should be called
            only from the `Dbf` instance.


        """
        self._validateIndex(False)
        self.dbf.stream.seek(self.position)
        self.dbf.stream.write(self.toString())
        # FIXME: may be move this write somewhere else?
        # why we should check this condition for each record?
        if self.index == len(self.dbf):
            # this is the last record,
            # we should write SUB (ASCII 26)
            self.dbf.stream.write("\x1A")

    ## utility methods

    def _validateIndex(self, allowUndefined=True, checkRange=False):
        """Valid ``self.index`` value.

        If ``allowUndefined`` argument is True functions does nothing
        in case of ``self.index`` pointing to None object.

        """
        if self.index is None:
            if not allowUndefined:
                raise ValueError("Index is undefined")
        elif self.index < 0:
            raise ValueError("Index can't be negative (%s)" % self.index)
        elif checkRange and self.index <= self.dbf.header.recordCount:
            raise ValueError("There are only %d records in the DBF" %
                self.dbf.header.recordCount)

    ## interface methods

    def store(self):
        """Store current record in the DBF.

        If ``self.index`` is None, this record will be appended to the
        records of the DBF this records belongs to; or replaced otherwise.

        """
        self._validateIndex()
        if self.index is None:
            self.index = len(self.dbf)
            self.dbf.append(self)
        else:
            self.dbf[self.index] = self

    def delete(self):
        """Mark method as deleted."""
        self.deleted = True

    def toString(self):
        """Return string packed record values."""
        return "".join([" *"[self.deleted]] + [
            _def.encodeValue(_dat, self.dbf)
            for (_def, _dat) in izip(self.dbf.header.fields, self.fieldData)
        ])

    def asList(self):
        """Return a flat list of fields.

        Note:
            Change of the list's values won't change
            real values stored in this object.

        """
        return self.fieldData[:]

    def asDict(self):
        """Return a dictionary of fields.

        Note:
            Change of the dicts's values won't change
            real values stored in this object.

        """
        return dict([_i for _i in izip(self.dbf.fieldNames, self.fieldData)])

    def __getitem__(self, key):
        """Return value by field name or field index."""
        if isinstance(key, (long, int)):
            # integer index of the field
            return self.fieldData[key]
        # assuming string field name
        elif isinstance(key, (list, tuple)):
            name, index = key
            return self.fieldData[self.dbf.indexOfFieldName(name)[index]]
        else:
            return self.fieldData[self.dbf.indexOfFieldName(key)]

    def __setitem__(self, key, value):
        """Set field value by integer index of the field or string name."""
        if isinstance(key, (int, long)):
            # integer index of the field
            self.fieldData[key] = value
        # assuming string field name
        elif isinstance(key, (list, tuple)):
            name, index = key
            self.fieldData[self.dbf.indexOfFieldName(key)[index]] = value
        else:
            self.fieldData[self.dbf.indexOfFieldName(key)] = value

# vim: et sts=4 sw=4: